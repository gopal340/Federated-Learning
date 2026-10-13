"""
ModelManager — loads all actual trained artifacts from the FINAL_FEDERATED_QWEN_JEV_V2 package.

Handles:
  - Qwen/Qwen2.5-0.5B-Instruct base model loading
  - LoRA adapter attachment (agent1, agent2, global_qwen)
  - JEV decision engine initialization with actual package artifacts
  - Memory-safe strategy: single base model with adapter swapping
"""
import os
import json
import time
import logging
import torch
from pathlib import Path
from typing import Dict, Optional
from inference.jev import JEVEngine

logger = logging.getLogger(__name__)


class ModelManager:
    """Manages loading and lifecycle of all model artifacts."""

    def __init__(self, artifacts_dir: str, device: str = "cuda"):
        self.artifacts_dir = Path(artifacts_dir)
        self.device = device if torch.cuda.is_available() and device == "cuda" else "cpu"
        self.base_model = None
        self.tokenizer = None
        self.adapters: Dict[str, object] = {}  # name -> PeftModel
        self.jev_engine: Optional[JEVEngine] = None
        self._loaded = False
        self._current_adapter: Optional[str] = None

        # Validate artifact directory
        if not self.artifacts_dir.exists():
            raise FileNotFoundError(f"Artifacts directory not found: {self.artifacts_dir}")

        logger.info(f"ModelManager initialized with artifacts_dir={self.artifacts_dir}, device={self.device}")

    def _verify_artifacts(self) -> Dict[str, bool]:
        """Verify that all expected artifacts exist before attempting load."""
        checks = {
            "qwen/agent1/adapter_config.json": (self.artifacts_dir / "qwen" / "agent1" / "adapter_config.json").exists(),
            "qwen/agent1/adapter_model.safetensors": (self.artifacts_dir / "qwen" / "agent1" / "adapter_model.safetensors").exists(),
            "qwen/agent2/adapter_config.json": (self.artifacts_dir / "qwen" / "agent2" / "adapter_config.json").exists(),
            "qwen/agent2/adapter_model.safetensors": (self.artifacts_dir / "qwen" / "agent2" / "adapter_model.safetensors").exists(),
            "qwen/global_qwen/adapter_config.json": (self.artifacts_dir / "qwen" / "global_qwen" / "adapter_config.json").exists(),
            "qwen/global_qwen/adapter_model.safetensors": (self.artifacts_dir / "qwen" / "global_qwen" / "adapter_model.safetensors").exists(),
            "jev/head.safetensors": (self.artifacts_dir / "jev" / "head.safetensors").exists(),
            "jev/calibration.json": (self.artifacts_dir / "jev" / "calibration.json").exists(),
            "jev/adapter_vllm/decision_head.json": (self.artifacts_dir / "jev" / "adapter_vllm" / "decision_head.json").exists(),
            "jev/adapter/adapter_model.safetensors": (self.artifacts_dir / "jev" / "adapter" / "adapter_model.safetensors").exists(),
        }

        for artifact, exists in checks.items():
            status = "✓" if exists else "✗ MISSING"
            logger.info(f"  {status} {artifact}")

        return checks

    def load_all(self):
        """Load all models and artifacts. Called once at startup."""
        if self._loaded:
            logger.info("Models already loaded, skipping.")
            return

        logger.info("=" * 60)
        logger.info("LOADING ALL MODEL ARTIFACTS")
        logger.info("=" * 60)

        # Step 1: Verify artifacts
        logger.info("Step 1: Verifying artifact files...")
        checks = self._verify_artifacts()
        missing = [k for k, v in checks.items() if not v]
        if missing:
            raise FileNotFoundError(
                f"Missing required artifacts: {missing}. "
                "Cannot proceed without actual trained model files."
            )
        logger.info("All artifacts verified ✓")

        # Step 2: Load base Qwen model + tokenizer
        logger.info("Step 2: Loading base model Qwen/Qwen2.5-0.5B-Instruct...")
        self._load_base_model()

        # Step 3: Load Qwen LoRA adapters
        logger.info("Step 3: Loading LoRA adapters...")
        self._load_qwen_adapters()

        # Step 4: Initialize JEV Decision Engine with actual package artifacts
        logger.info("Step 4: Initializing JEV Decision Engine with actual artifacts...")
        self.jev_engine = JEVEngine(self.artifacts_dir)

        self._loaded = True
        logger.info("=" * 60)
        logger.info("ALL MODELS LOADED SUCCESSFULLY")
        logger.info("=" * 60)

    def _load_base_model(self):
        """Load the base Qwen2.5-0.5B-Instruct model."""
        from transformers import AutoModelForCausalLM, AutoTokenizer

        model_id = "Qwen/Qwen2.5-0.5B-Instruct"
        start = time.time()

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_id,
            trust_remote_code=True,
            padding_side="left"
        )
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        dtype = torch.float16 if self.device == "cuda" else torch.float32
        self.base_model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=dtype,
            device_map=self.device if self.device == "cuda" else None,
            trust_remote_code=True,
        )
        if self.device == "cpu":
            self.base_model = self.base_model.to(self.device)

        self.base_model.eval()
        elapsed = time.time() - start
        logger.info(f"  Base model loaded in {elapsed:.1f}s on {self.device}")

    def _load_qwen_adapters(self):
        """Load all three LoRA adapters from actual safetensors files."""
        from peft import PeftModel

        adapter_names = {
            "agent1": self.artifacts_dir / "qwen" / "agent1",
            "agent2": self.artifacts_dir / "qwen" / "agent2",
            "global_qwen": self.artifacts_dir / "qwen" / "global_qwen",
        }

        first_name = "global_qwen"
        first_path = adapter_names[first_name]

        start = time.time()
        self.base_model = PeftModel.from_pretrained(
            self.base_model,
            str(first_path),
            adapter_name=first_name,
        )
        elapsed = time.time() - start
        self.adapters[first_name] = True
        logger.info(f"  Loaded adapter '{first_name}' from {first_path} in {elapsed:.1f}s")

        for name, path in adapter_names.items():
            if name == first_name:
                continue
            start = time.time()
            self.base_model.load_adapter(str(path), adapter_name=name)
            elapsed = time.time() - start
            self.adapters[name] = True
            logger.info(f"  Loaded adapter '{name}' from {path} in {elapsed:.1f}s")

        self.base_model.set_adapter("global_qwen")
        self._current_adapter = "global_qwen"
        logger.info(f"  Active adapter: global_qwen")

    def set_adapter(self, adapter_name: str):
        """Switch the active LoRA adapter on the shared base model."""
        if adapter_name not in self.adapters:
            raise ValueError(f"Unknown adapter: {adapter_name}. Available: {list(self.adapters.keys())}")
        if self._current_adapter != adapter_name:
            self.base_model.set_adapter(adapter_name)
            self._current_adapter = adapter_name
            logger.debug(f"Switched to adapter: {adapter_name}")

    def get_model_info(self) -> dict:
        """Return model loading status information."""
        jev_details = self.jev_engine.get_artifact_details() if self.jev_engine else {}
        return {
            "base_model": "Qwen/Qwen2.5-0.5B-Instruct",
            "fine_tuning": "LoRA / PEFT",
            "federated_algorithm": "FedAvg",
            "num_agents": 2,
            "dataset": "FinGPT/fingpt-fiqa_qa",
            "decision_model": "autotrust/JEV-9B",
            "qwen_adapters_loaded": {k: v for k, v in self.adapters.items()},
            "jev_artifacts": jev_details,
            "device": self.device,
            "raw_training_data_included": False,
            "base_model_weights_included": False,
        }

    @property
    def is_loaded(self) -> bool:
        return self._loaded
