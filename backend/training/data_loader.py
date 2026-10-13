"""
Data Loader for Federated Financial Fraud & Banking Risk Training.

Downloads the FinGPT Financial QA dataset (or compatible financial risk datasets)
from HuggingFace and prepares federated data partitions for:
  - Agent 1: Fraud Detection & Transaction Analyst
  - Agent 2: Risk Governance & AML Officer

Dataset: FinGPT/fingpt-fiqa_qa (HuggingFace)
Domain:  Banking, Payment Fraud, AML, Credit Risk, Transaction Anomaly Detection
"""
import logging
import random
from typing import Dict, List, Tuple, Optional
from datasets import load_dataset, Dataset

logger = logging.getLogger(__name__)

# ── Dataset Constants ────────────────────────────────────────────────────────
DATASET_ID = "FinGPT/fingpt-fiqa_qa"

# Role-specific system prompts injected during training so that each agent
# learns to reason in its designated domain persona.
AGENT1_TRAINING_SYSTEM_PROMPT = (
    "You are Agent 1 — the Fraud Detection & Transaction Analyst in a multi-agent "
    "federated decision intelligence system for banking and financial risk.\n\n"
    "Your role is to provide rigorous, evidence-based analysis of financial scenarios, "
    "transaction telemetry, and potential fraud patterns. You must:\n"
    "1. IDENTIFY anomalous transaction patterns, velocity spikes, and fraud indicators\n"
    "2. ASSESS risk factors — evaluating both fraudulent signals and legitimate customer explanations\n"
    "3. EVALUATE the likelihood of unauthorized transactions, identity theft, or payment fraud\n"
    "4. WEIGH transaction risk against normal cardholder / merchant behavior\n"
    "5. PROVIDE a clear recommendation (APPROVE, CHALLENGE with MFA/OTP, ESCALATE to human investigator, or BLOCK)\n\n"
    "Be specific, analytical, and data-driven. Conclude with a definitive stance: "
    "TRUE (high fraud/financial risk confirmed) or FALSE (legitimate transaction/low risk)."
)

AGENT2_TRAINING_SYSTEM_PROMPT = (
    "You are Agent 2 — the Risk Governance & Anti-Money Laundering (AML) Officer in a multi-agent "
    "federated decision intelligence system for banking and financial risk.\n\n"
    "Your role is to critically audit financial scenarios by challenging assumptions, assessing "
    "regulatory compliance (BSA/AML), credit exposure, and customer friction. You must:\n"
    "1. CHALLENGE initial fraud assumptions — could this be legitimate travel or high-net-worth spending?\n"
    "2. AUDIT regulatory compliance, BSA/AML structuring, and sanction risk indicators\n"
    "3. FLAG missing telemetry or customer verification history\n"
    "4. ASSESS uncertainty and weigh financial loss against false-positive customer friction\n"
    "5. EVALUATE potential for false positives/negatives in automated fraud models\n"
    "6. PROVIDE an independent recommendation (APPROVE, CHALLENGE with MFA/OTP, ESCALATE, or BLOCK)\n\n"
    "Be skeptical, thorough, and constructive. Conclude with a definitive stance: "
    "TRUE (high fraud/financial risk confirmed) or FALSE (legitimate transaction/low risk)."
)


def download_dataset(
    dataset_id: str = DATASET_ID,
    max_samples: Optional[int] = None,
    seed: int = 42,
) -> Dataset:
    """
    Download the financial instruction dataset from HuggingFace.

    Args:
        dataset_id: HuggingFace dataset identifier (default: FinGPT/fingpt-fiqa_qa).
        max_samples: Optional cap on total samples (None = use all).
        seed: Random seed for reproducibility.

    Returns:
        HuggingFace Dataset object.
    """
    logger.info(f"Downloading financial dataset: {dataset_id}")
    try:
        ds = load_dataset(dataset_id, split="train")
    except Exception as e:
        logger.warning(f"Failed to load split 'train' directly ({e}), trying default split")
        loaded = load_dataset(dataset_id)
        first_split = list(loaded.keys())[0]
        ds = loaded[first_split]

    logger.info(f"  Raw dataset size: {len(ds)} samples")

    if max_samples and len(ds) > max_samples:
        ds = ds.shuffle(seed=seed).select(range(max_samples))
        logger.info(f"  Capped to {max_samples} samples")

    return ds


def _extract_conversation_text(sample: dict) -> Tuple[str, str]:
    """
    Extract the user question/instruction and assistant answer from a dataset sample.

    Supports multiple formats:
      1. FinGPT format: 'instruction', 'input', 'output'
      2. ChatML format: 'messages' list with 'role' and 'content'
      3. QA format: 'question', 'context', 'answer'
      4. Generic format: 'instruction' / 'response', 'prompt' / 'completion'

    Returns:
        (user_text, assistant_text) tuple.
    """
    # Format 1: FinGPT (instruction, input, output)
    if "instruction" in sample and "output" in sample:
        instr = str(sample.get("instruction") or "").strip()
        inp = str(sample.get("input") or "").strip()
        out = str(sample.get("output") or "").strip()
        if inp:
            user_text = f"{instr}\n\nContext / Transaction Data:\n{inp}"
        else:
            user_text = instr
        return user_text.strip(), out.strip()

    # Format 2: ChatML messages
    messages = sample.get("messages", [])
    if isinstance(messages, list) and len(messages) > 0:
        user_text = ""
        assistant_text = ""
        for msg in messages:
            role = msg.get("role", "").lower()
            content = msg.get("content", "").strip()
            if role == "user" and not user_text:
                user_text = content
            elif role == "assistant" and not assistant_text:
                assistant_text = content
        if user_text and assistant_text:
            return user_text.strip(), assistant_text.strip()

    # Format 3: Financial QA (question, context, answer)
    if "question" in sample and "answer" in sample:
        q = str(sample.get("question") or "").strip()
        ctx = str(sample.get("context") or "").strip()
        ans = str(sample.get("answer") or "").strip()
        if ctx:
            user_text = f"{q}\n\nFinancial Context:\n{ctx}"
        else:
            user_text = q
        return user_text.strip(), ans.strip()

    # Format 4: Prompt / completion or Instruction / response
    user_text = str(
        sample.get("prompt")
        or sample.get("instruction")
        or sample.get("input")
        or ""
    ).strip()
    assistant_text = str(
        sample.get("completion")
        or sample.get("response")
        or sample.get("output")
        or ""
    ).strip()

    return user_text, assistant_text


def prepare_federated_partitions(
    dataset: Dataset,
    agent1_fraction: float = 0.5,
    seed: int = 42,
) -> Tuple[List[dict], List[dict]]:
    """
    Split the dataset into two non-overlapping partitions simulating
    federated financial institutions (Agent 1: Fraud, Agent 2: Risk/AML).

    Each partition injects the agent's role-specific system prompt so the
    LoRA adapter learns the designated banking reasoning style.

    Args:
        dataset: HuggingFace Dataset.
        agent1_fraction: Fraction of data allocated to Agent 1.
        seed: Random seed.

    Returns:
        (agent1_samples, agent2_samples) — lists of chat-formatted dicts.
    """
    random.seed(seed)
    indices = list(range(len(dataset)))
    random.shuffle(indices)

    split_point = int(len(indices) * agent1_fraction)
    agent1_indices = indices[:split_point]
    agent2_indices = indices[split_point:]

    logger.info(
        f"Federated partition: Agent 1 = {len(agent1_indices)} samples, "
        f"Agent 2 = {len(agent2_indices)} samples"
    )

    def build_samples(idx_list: List[int], system_prompt: str) -> List[dict]:
        samples = []
        skipped = 0
        for idx in idx_list:
            user_text, assistant_text = _extract_conversation_text(dataset[idx])

            if not user_text or not assistant_text:
                skipped += 1
                continue

            # ChatML conversation format — native to Qwen2.5
            sample = {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_text},
                    {"role": "assistant", "content": assistant_text},
                ]
            }
            samples.append(sample)

        if skipped:
            logger.warning(f"  Skipped {skipped} samples with empty user/assistant text")
        return samples

    agent1_samples = build_samples(agent1_indices, AGENT1_TRAINING_SYSTEM_PROMPT)
    agent2_samples = build_samples(agent2_indices, AGENT2_TRAINING_SYSTEM_PROMPT)

    logger.info(
        f"Prepared: Agent 1 = {len(agent1_samples)} usable samples, "
        f"Agent 2 = {len(agent2_samples)} usable samples"
    )

    return agent1_samples, agent2_samples


def format_for_tokenizer(samples: List[dict], tokenizer) -> Dataset:
    """
    Convert chat-formatted samples into tokenized training examples
    using the Qwen chat template.

    Args:
        samples: List of chat dicts with 'messages' field.
        tokenizer: The Qwen tokenizer with chat template support.

    Returns:
        HuggingFace Dataset ready for SFTTrainer.
    """
    texts = []
    for sample in samples:
        text = tokenizer.apply_chat_template(
            sample["messages"],
            tokenize=False,
            add_generation_prompt=False,
        )
        texts.append(text)

    return Dataset.from_dict({"text": texts})
