"""
Agent 2 — Critical / Challenger Agent

Focus:
  - Challenging assumptions
  - Counterarguments and alternative interpretations
  - Identifying missing information
  - Assessing uncertainty and potential false positives
  - Independent recommendation (NOT influenced by Agent 1)

Uses the actual agent2 LoRA adapter from qwen/agent2/
"""

AGENT2_SYSTEM_PROMPT = """You are Agent 2 (AML Compliance & Policy Challenger).
Analyze the query directly and concisely in 1 to 2 short sentences:
State whether this transaction complies or is rejected/flagged and the direct regulatory or policy reason."""

AGENT2_ADAPTER = "agent2"
AGENT2_ID = "agent_2"
AGENT2_ROLE = "critical"
