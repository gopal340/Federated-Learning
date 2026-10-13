"""
Federated LoRA Trainer with FedAvg Aggregation.

Implements the complete federated training lifecycle:
  1. Load base Qwen2.5-0.5B-Instruct model
  2. Train Agent 1 LoRA adapter on its private partition
  3. Train Agent 2 LoRA adapter on its private partition
  4. Aggregate via FedAvg → produce the global_qwen adapter
  5. Save all three adapters as .safetensors files

This trains domain-specific LoRA adapters for Financial Fraud Detection
and Banking Risk Intelligence using federated learning.
"""
import os
import sys
import copy
import time
import logging
import torch
from pathlib import Path

# Ensure backend and training directories are in sys.path regardless of where python is executed
_CURRENT_DIR = Path(__file__).resolve().parent
_BACKEND_DIR = _CURRENT_DIR.parent
for _p in [str(_BACKEND_DIR), str(_CURRENT_DIR)]:
    if _p not in sys.path:
        sys.path.insert(0, _p)
from typing import Dict, List, Optional, Tuple
from collections import OrderedDict

from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model, PeftModel
try:
    from trl import SFTTrainer, SFTConfig
    HAS_SFT_CONFIG = True
except ImportError:
    from trl import SFTTrainer
    HAS_SFT_CONFIG = False
from datasets import Dataset

logger = logging.getLogger(__name__)


# ── LoRA Configuration (matches existing adapter_config.json) ────────────────
def get_lora_config() -> LoraConfig:
    """
    Create the LoRA configuration matching the project's existing adapters.

    Based on the actual adapter_config.json found in qwen/agent1/:
      - r=8, lora_alpha=16, dropout=0.05
      - target_modules: q_proj, k_proj, v_proj, o_proj
      - task_type: CAUSAL_LM
    """
    return LoraConfig(
        r=8,
        lora_alpha=16,
        lora_dropout=0.05,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        task_type="CAUSAL_LM",
        bias="none",
    )


# ── Base Model Loading ───────────────────────────────────────────────────────
def load_base_model_and_tokenizer(
    model_id: str = "Qwen/Qwen2.5-0.5B-Instruct",
    device: str = "cuda",
) -> Tuple:
    """
    Load the base Qwen model and tokenizer for training.

    Args:
        model_id: HuggingFace model identifier.
        device: Target device ('cuda' or 'cpu').

    Returns:
        (model, tokenizer) tuple.
    """
    use_cuda = device == "cuda" and torch.cuda.is_available()
    dtype = torch.float16 if use_cuda else torch.float32

    logger.info(f"Loading base model: {model_id}")
    logger.info(f"  Device: {'cuda' if use_cuda else 'cpu'}, dtype: {dtype}")

    tokenizer = AutoTokenizer.from_pretrained(
        model_id,
        trust_remote_code=True,
        padding_side="right",  # Right padding for training
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=dtype,
        device_map="auto" if use_cuda else None,
        trust_remote_code=True,
    )

    if not use_cuda:
        model = model.to("cpu")

    logger.info(f"  Base model loaded: {sum(p.numel() for p in model.parameters()) / 1e6:.1f}M parameters")
    return model, tokenizer


# ── Single Agent LoRA Training ───────────────────────────────────────────────
def train_agent_lora(
    base_model,
    tokenizer,
    train_dataset: Dataset,
    output_dir: str,
    agent_name: str,
    num_epochs: int = 3,
    batch_size: int = 4,
    learning_rate: float = 2e-4,
    max_seq_length: int = 1024,
    gradient_accumulation_steps: int = 4,
    warmup_ratio: float = 0.05,
    logging_steps: int = 10,
    save_steps: int = 100,
) -> PeftModel:
    """
    Train a LoRA adapter for a single agent on its private data partition.

    Args:
        base_model: The base Qwen model (will be wrapped with LoRA).
        tokenizer: Qwen tokenizer.
        train_dataset: HuggingFace Dataset with 'text' column.
        output_dir: Directory to save the trained adapter.
        agent_name: Identifier for logging ('agent1' or 'agent2').
        num_epochs: Number of training epochs.
        batch_size: Per-device batch size.
        learning_rate: Learning rate for AdamW.
        max_seq_length: Maximum sequence length for tokenization.
        gradient_accumulation_steps: Gradient accumulation steps.
        warmup_ratio: Warmup fraction of total steps.
        logging_steps: Log every N steps.
        save_steps: Save checkpoint every N steps.

    Returns:
        Trained PeftModel.
    """
    logger.info(f"\n{'='*60}")
    logger.info(f"TRAINING: {agent_name.upper()} LoRA ADAPTER")
    logger.info(f"{'='*60}")
    logger.info(f"  Dataset size: {len(train_dataset)} samples")
    logger.info(f"  Epochs: {num_epochs}, Batch size: {batch_size}")
    logger.info(f"  Learning rate: {learning_rate}")
    logger.info(f"  Output: {output_dir}")

    # Create a fresh copy of the base model for each agent
    # (prevents adapter cross-contamination during federated training)
    model_copy = copy.deepcopy(base_model)

    # Apply LoRA
    lora_config = get_lora_config()
    peft_model = get_peft_model(model_copy, lora_config)

    trainable_params = sum(p.numel() for p in peft_model.parameters() if p.requires_grad)
    total_params = sum(p.numel() for p in peft_model.parameters())
    logger.info(
        f"  LoRA applied: {trainable_params / 1e6:.2f}M trainable / "
        f"{total_params / 1e6:.1f}M total ({100 * trainable_params / total_params:.2f}%)"
    )

    # Calculate warmup steps
    warmup_steps = max(1, int(warmup_ratio * 100))

    # Training arguments / configuration
    if HAS_SFT_CONFIG:
        training_args = SFTConfig(
            output_dir=output_dir,
            num_train_epochs=num_epochs,
            per_device_train_batch_size=batch_size,
            gradient_accumulation_steps=gradient_accumulation_steps,
            learning_rate=learning_rate,
            warmup_steps=warmup_steps,
            weight_decay=0.01,
            logging_steps=logging_steps,
            save_steps=save_steps,
            save_total_limit=2,
            fp16=torch.cuda.is_available(),
            bf16=False,
            optim="adamw_torch",
            lr_scheduler_type="cosine",
            report_to="none",  # Disable wandb/tensorboard
            remove_unused_columns=False,
            dataloader_pin_memory=False,
            seed=42,
            max_length=max_seq_length,
            dataset_text_field="text",
        )
        trainer = SFTTrainer(
            model=peft_model,
            args=training_args,
            train_dataset=train_dataset,
            processing_class=tokenizer,
        )
    else:
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=num_epochs,
            per_device_train_batch_size=batch_size,
            gradient_accumulation_steps=gradient_accumulation_steps,
            learning_rate=learning_rate,
            warmup_steps=warmup_steps,
            weight_decay=0.01,
            logging_steps=logging_steps,
            save_steps=save_steps,
            save_total_limit=2,
            fp16=torch.cuda.is_available(),
            bf16=False,
            optim="adamw_torch",
            lr_scheduler_type="cosine",
            report_to="none",
            remove_unused_columns=False,
            dataloader_pin_memory=False,
            seed=42,
        )
        trainer = SFTTrainer(
            model=peft_model,
            args=training_args,
            train_dataset=train_dataset,
            processing_class=tokenizer,
            max_seq_length=max_seq_length,
        )

    # Train
    start = time.time()
    train_result = trainer.train()
    elapsed = time.time() - start

    logger.info(f"  Training completed in {elapsed:.1f}s")
    logger.info(f"  Final loss: {train_result.training_loss:.4f}")

    # Save the adapter (only LoRA weights, not the full model)
    peft_model.save_pretrained(output_dir)
    logger.info(f"  Adapter saved to: {output_dir}")

    return peft_model


# ── FedAvg Aggregation ───────────────────────────────────────────────────────
def fedavg_aggregate(
    adapter_dirs: List[str],
    output_dir: str,
    weights: Optional[List[float]] = None,
) -> str:
    """
    Federated Averaging (FedAvg) of multiple LoRA adapters.

    Loads the adapter_model.safetensors from each agent's directory,
    computes the weighted average of all LoRA parameters, and saves
    the result as the global_qwen adapter.

    Args:
        adapter_dirs: List of paths to trained agent adapter directories.
        output_dir: Directory to save the aggregated global adapter.
        weights: Optional per-agent weights (defaults to equal weighting).

    Returns:
        Path to the saved global adapter directory.
    """
    from safetensors.torch import load_file, save_file
    import json

    logger.info(f"\n{'='*60}")
    logger.info(f"FEDAVG AGGREGATION")
    logger.info(f"{'='*60}")
    logger.info(f"  Input adapters: {adapter_dirs}")
    logger.info(f"  Output: {output_dir}")

    n_agents = len(adapter_dirs)
    if weights is None:
        weights = [1.0 / n_agents] * n_agents
    else:
        # Normalize weights
        total_w = sum(weights)
        weights = [w / total_w for w in weights]

    logger.info(f"  Weights: {weights}")

    # Load all adapter state dicts
    state_dicts = []
    for adapter_dir in adapter_dirs:
        safetensors_path = os.path.join(adapter_dir, "adapter_model.safetensors")
        if not os.path.exists(safetensors_path):
            raise FileNotFoundError(f"Adapter not found: {safetensors_path}")
        sd = load_file(safetensors_path)
        state_dicts.append(sd)
        logger.info(f"  Loaded adapter from {adapter_dir}: {len(sd)} parameter tensors")

    # Verify all adapters have the same parameter keys
    keys = set(state_dicts[0].keys())
    for i, sd in enumerate(state_dicts[1:], 1):
        if set(sd.keys()) != keys:
            missing = keys - set(sd.keys())
            extra = set(sd.keys()) - keys
            logger.warning(
                f"  Adapter {i} has mismatched keys. "
                f"Missing: {missing}, Extra: {extra}"
            )

    # Compute weighted average for each parameter
    aggregated = OrderedDict()
    for key in keys:
        stacked = torch.stack([sd[key].float() for sd in state_dicts])
        weight_tensor = torch.tensor(weights, dtype=torch.float32).view(-1, *([1] * (stacked.dim() - 1)))
        avg = (stacked * weight_tensor).sum(dim=0)
        aggregated[key] = avg.to(state_dicts[0][key].dtype)

    # Save aggregated adapter
    os.makedirs(output_dir, exist_ok=True)

    # Save safetensors
    output_safetensors = os.path.join(output_dir, "adapter_model.safetensors")
    save_file(aggregated, output_safetensors)
    logger.info(f"  Aggregated adapter saved: {output_safetensors}")

    # Copy adapter_config.json from the first agent (all should be identical)
    config_src = os.path.join(adapter_dirs[0], "adapter_config.json")
    config_dst = os.path.join(output_dir, "adapter_config.json")
    if os.path.exists(config_src):
        import shutil
        shutil.copy2(config_src, config_dst)
        logger.info(f"  Adapter config copied to: {config_dst}")

    logger.info(f"  FedAvg aggregation complete. Global adapter saved at: {output_dir}")
    return output_dir


# ── Full Federated Training Pipeline ─────────────────────────────────────────
def run_federated_training(
    output_base_dir: str,
    model_id: str = "Qwen/Qwen2.5-0.5B-Instruct",
    device: str = "cuda",
    max_samples: Optional[int] = None,
    num_epochs: int = 3,
    batch_size: int = 4,
    learning_rate: float = 2e-4,
    max_seq_length: int = 1024,
    seed: int = 42,
) -> Dict[str, str]:
    """
    Execute the complete federated training pipeline:
      1. Download & partition the financial fraud & risk dataset
      2. Train Agent 1 LoRA adapter
      3. Train Agent 2 LoRA adapter
      4. Run FedAvg aggregation → global_qwen adapter

    Args:
        output_base_dir: Base directory for all outputs (will contain qwen/agent1, qwen/agent2, qwen/global_qwen).
        model_id: HuggingFace model ID for base model.
        device: Training device ('cuda' or 'cpu').
        max_samples: Optional cap on total dataset size.
        num_epochs: Training epochs per agent.
        batch_size: Per-device batch size.
        learning_rate: Learning rate.
        max_seq_length: Maximum sequence length.
        seed: Random seed.

    Returns:
        Dict with paths to all saved adapters.
    """
    try:
        from training.data_loader import (
            download_dataset,
            prepare_federated_partitions,
            format_for_tokenizer,
        )
    except ModuleNotFoundError:
        from data_loader import (
            download_dataset,
            prepare_federated_partitions,
            format_for_tokenizer,
        )

    total_start = time.time()
    output_base = Path(output_base_dir)
    agent1_dir = str(output_base / "qwen" / "agent1")
    agent2_dir = str(output_base / "qwen" / "agent2")
    global_dir = str(output_base / "qwen" / "global_qwen")

    logger.info("=" * 60)
    logger.info("FEDERATED TRAINING PIPELINE -- START")
    logger.info("=" * 60)
    logger.info(f"  Base model: {model_id}")
    logger.info(f"  Output: {output_base_dir}")
    logger.info(f"  Device: {device}")
    logger.info(f"  Max samples: {max_samples or 'ALL'}")

    # Step 1: Data
    logger.info("\n[Step 1] Downloading & partitioning dataset")
    raw_dataset = download_dataset(max_samples=max_samples, seed=seed)
    agent1_samples, agent2_samples = prepare_federated_partitions(
        raw_dataset, agent1_fraction=0.5, seed=seed,
    )

    # Step 2: Load base model
    logger.info("\n[Step 2] Loading base model")
    base_model, tokenizer = load_base_model_and_tokenizer(model_id, device)

    # Step 3: Tokenize partitions
    logger.info("\n[Step 3] Tokenizing partitions")
    agent1_dataset = format_for_tokenizer(agent1_samples, tokenizer)
    agent2_dataset = format_for_tokenizer(agent2_samples, tokenizer)
    logger.info(f"  Agent 1: {len(agent1_dataset)} tokenized samples")
    logger.info(f"  Agent 2: {len(agent2_dataset)} tokenized samples")

    # Step 4: Train Agent 1
    logger.info("\n[Step 4] Training Agent 1 (Fraud Analyst)")
    train_agent_lora(
        base_model=base_model,
        tokenizer=tokenizer,
        train_dataset=agent1_dataset,
        output_dir=agent1_dir,
        agent_name="agent1",
        num_epochs=num_epochs,
        batch_size=batch_size,
        learning_rate=learning_rate,
        max_seq_length=max_seq_length,
    )

    # Step 5: Train Agent 2
    logger.info("\n[Step 5] Training Agent 2 (Risk/AML Officer)")
    train_agent_lora(
        base_model=base_model,
        tokenizer=tokenizer,
        train_dataset=agent2_dataset,
        output_dir=agent2_dir,
        agent_name="agent2",
        num_epochs=num_epochs,
        batch_size=batch_size,
        learning_rate=learning_rate,
        max_seq_length=max_seq_length,
    )

    # Step 6: FedAvg Aggregation
    logger.info("\n[Step 6] FedAvg Aggregation")
    fedavg_aggregate(
        adapter_dirs=[agent1_dir, agent2_dir],
        output_dir=global_dir,
        weights=[1.0, 1.0],  # Equal weighting
    )

    total_elapsed = time.time() - total_start
    logger.info(f"\n{'='*60}")
    logger.info(f"FEDERATED TRAINING COMPLETE -- {total_elapsed:.1f}s total")
    logger.info(f"{'='*60}")
    logger.info(f"  Agent 1 adapter: {agent1_dir}")
    logger.info(f"  Agent 2 adapter: {agent2_dir}")
    logger.info(f"  Global adapter:  {global_dir}")

    return {
        "agent1": agent1_dir,
        "agent2": agent2_dir,
        "global_qwen": global_dir,
        "total_time_s": total_elapsed,
    }
