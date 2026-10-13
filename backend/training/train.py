"""
Federated Training Entry Point.

Usage:
  # Full training with default settings (all dataset samples, 3 epochs)
  python -m training.train

  # Quick test with 200 samples and 1 epoch
  python -m training.train --max-samples 200 --epochs 1

  # Custom output directory
  python -m training.train --output ./my_trained_models

  # CPU-only training
  python -m training.train --device cpu --max-samples 500 --epochs 1 --batch-size 2

Arguments:
  --output       Output directory for trained adapters (default: ../FINAL_FEDERATED_QWEN_JEV_V2)
  --model        Base model ID (default: Qwen/Qwen2.5-0.5B-Instruct)
  --device       Training device: cuda or cpu (default: cuda)
  --max-samples  Max total dataset samples, None = use all (default: 2000)
  --epochs       Training epochs per agent (default: 3)
  --batch-size   Per-device batch size (default: 4)
  --lr           Learning rate (default: 2e-4)
  --max-seq-len  Maximum sequence length (default: 1024)
  --seed         Random seed (default: 42)
"""
import os
import sys
import argparse
import logging
from pathlib import Path

# Ensure backend and training directories are in sys.path regardless of where python is executed
_CURRENT_DIR = Path(__file__).resolve().parent
_BACKEND_DIR = _CURRENT_DIR.parent
for _p in [str(_BACKEND_DIR), str(_CURRENT_DIR)]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

# Force UTF-8 on Windows consoles to prevent cp1252 charmap encoding errors
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("training.log", mode="w", encoding="utf-8"),
    ],
)
logger = logging.getLogger("train")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Federated LoRA Training for Financial Fraud & Risk Decision Intelligence",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output directory for trained adapters. Default: ../FINAL_FEDERATED_QWEN_JEV_V2",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="Qwen/Qwen2.5-0.5B-Instruct",
        help="Base model HuggingFace ID",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda",
        choices=["cuda", "cpu"],
        help="Training device",
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        default=None,
        help="Max dataset samples (default: None = train on ALL samples)",
    )
    parser.add_argument(
        "--all-samples",
        action="store_true",
        default=True,
        help="Train on all samples in the dataset without cap (default: True)",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=3,
        help="Training epochs per agent",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=4,
        help="Per-device training batch size",
    )
    parser.add_argument(
        "--lr",
        type=float,
        default=2e-4,
        help="Learning rate",
    )
    parser.add_argument(
        "--max-seq-len",
        type=int,
        default=1024,
        help="Maximum sequence length for tokenization",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    # Determine sample count: None or <= 0 means train on ALL samples
    max_samples = None if (args.max_samples is None or args.max_samples <= 0) else args.max_samples

    # Resolve output directory
    if args.output is None:
        # Default: the FINAL_FEDERATED_QWEN_JEV_V2 artifacts directory
        backend_dir = Path(__file__).resolve().parent.parent
        output_dir = str(backend_dir.parent / "FINAL_FEDERATED_QWEN_JEV_V2")
    else:
        output_dir = args.output

    samples_display = "ALL (complete ~17,110 dataset)" if max_samples is None else str(max_samples)

    logger.info("=" * 70)
    logger.info("  FEDERATED FINANCIAL FRAUD & RISK LoRA TRAINING")
    logger.info("  Dataset: FinGPT/fingpt-fiqa_qa")
    logger.info("=" * 70)
    logger.info(f"  Output dir:     {output_dir}")
    logger.info(f"  Base model:     {args.model}")
    logger.info(f"  Device:         {args.device}")
    logger.info(f"  Max samples:    {samples_display}")
    logger.info(f"  Epochs:         {args.epochs}")
    logger.info(f"  Batch size:     {args.batch_size}")
    logger.info(f"  Learning rate:  {args.lr}")
    logger.info(f"  Max seq length: {args.max_seq_len}")
    logger.info(f"  Seed:           {args.seed}")
    logger.info("")

    # Import and run
    try:
        from training.federated_trainer import run_federated_training
    except ModuleNotFoundError:
        from federated_trainer import run_federated_training

    results = run_federated_training(
        output_base_dir=output_dir,
        model_id=args.model,
        device=args.device,
        max_samples=max_samples,
        num_epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.lr,
        max_seq_length=args.max_seq_len,
        seed=args.seed,
    )

    logger.info("\n" + "=" * 70)
    logger.info("  TRAINING RESULTS")
    logger.info("=" * 70)
    for key, value in results.items():
        logger.info(f"  {key}: {value}")

    logger.info("\n  ✓ All adapters trained and saved successfully!")
    logger.info(f"  ✓ Total training time: {results['total_time_s']:.1f} seconds")
    logger.info("")
    logger.info("  Next steps:")
    logger.info("    1. Restart the backend server to load the new adapters")
    logger.info("    2. The new fraud & banking risk-trained agents will be active")
    logger.info("    3. Try queries like: 'Does this rapid international wire transfer require fraud investigation?'")
    logger.info("")


if __name__ == "__main__":
    main()
