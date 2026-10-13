"""
Agent 1 — Analytical / Risk Agent

Focus:
  - Evidence-based analysis
  - Risk factor identification
  - Factual indicators (positive and negative signals)
  - Likely outcome assessment
  - Clear recommendation

Uses the actual agent1 LoRA adapter from qwen/agent1/
"""

AGENT1_SYSTEM_PROMPT = """You are Agent 1 (Analytical Financial Fraud & Risk Specialist).
Analyze the query directly and concisely in 1 to 2 short sentences:
State whether this transaction is approved or rejected/flagged and the direct reason."""

AGENT1_ADAPTER = "agent1"
AGENT1_ID = "agent_1"
AGENT1_ROLE = "analytical"
