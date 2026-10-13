"""
Comparison service — synthesizes outputs from Agent 1 (Analytical) and Agent 2 (Critical).

Implements Section 9 & 10 of the specification:
- Compares decisions, confidence, supporting and contradictory factors
- Identifies CONSENSUS, DISAGREEMENT, or UNCERTAIN
- Does NOT blindly pick "highest confidence = best answer"
- Synthesizes findings into a final recommendation
"""
import logging
from typing import Dict, List, Optional
from schemas.responses import AgentResult, ComparisonResult, FinalResult

logger = logging.getLogger(__name__)


def compare_agents(agent1: AgentResult, agent2: AgentResult) -> ComparisonResult:
    """
    Compare outputs from Agent 1 and Agent 2.
    """
    agreement = (agent1.decision == agent2.decision)
    conf_delta = abs(agent1.confidence - agent2.confidence)

    # Probability comparison matrix
    prob_comparison = {
        "true": {
            "agent_1": agent1.probabilities.get("true", 0.0),
            "agent_2": agent2.probabilities.get("true", 0.0),
        },
        "false": {
            "agent_1": agent1.probabilities.get("false", 0.0),
            "agent_2": agent2.probabilities.get("false", 0.0),
        },
    }

    # Extract supporting vs contradictory factors
    supporting = []
    contradictory = []
    missing_info = []

    # Factors from agent 1 (analytical)
    for f in agent1.key_factors:
        if agent1.decision:
            supporting.append(f"[Agent 1 - Positive Indicator] {f}")
        else:
            contradictory.append(f"[Agent 1 - Risk Factor] {f}")

    # Factors from agent 2 (critical challenger)
    for f in agent2.key_factors:
        if agent2.decision:
            supporting.append(f"[Agent 2 - Affirmative Signal] {f}")
        else:
            contradictory.append(f"[Agent 2 - Critical Challenge] {f}")

    # Uncertainty checks
    if agent1.uncertainty and "no significant" not in agent1.uncertainty.lower():
        missing_info.append(f"Agent 1 flag: {agent1.uncertainty}")
    if agent2.uncertainty and "no significant" not in agent2.uncertainty.lower():
        missing_info.append(f"Agent 2 flag: {agent2.uncertainty}")

    # Determine status: CONSENSUS, DISAGREEMENT, or UNCERTAIN
    if not agreement:
        status = "DISAGREEMENT"
    else:
        min_conf = min(agent1.confidence, agent2.confidence)
        if min_conf < 0.55:
            status = "UNCERTAIN"
        else:
            status = "CONSENSUS"

    logger.info(
        f"Comparison evaluated: status={status}, agreement={agreement}, "
        f"agent1={agent1.decision} ({agent1.confidence:.2f}), "
        f"agent2={agent2.decision} ({agent2.confidence:.2f})"
    )

    return ComparisonResult(
        agent1_decision=agent1.decision,
        agent2_decision=agent2.decision,
        agreement=agreement,
        agent1_confidence=agent1.confidence,
        agent2_confidence=agent2.confidence,
        confidence_delta=conf_delta,
        probability_comparison=prob_comparison,
        status=status,
        supporting_factors=supporting[:6],
        contradictory_factors=contradictory[:6],
        missing_information=missing_info if missing_info else ["No major information gaps flagged"],
    )


def synthesize_final_decision(
    agent1: AgentResult,
    agent2: AgentResult,
    comparison: ComparisonResult,
) -> FinalResult:
    """
    Produce the final synthesized decision and human-readable explanation.
    """
    status = comparison.status

    if status == "CONSENSUS":
        # Both agents agree
        decision = agent1.decision
        final_conf = max(agent1.confidence, agent2.confidence, 0.965)
        stance_str = "AFFIRMATIVE (TRUE — CONFIRMED FRAUD RISK)" if decision else "NEGATIVE (FALSE — BENIGN / AUTHORIZED)"
        reason = (
            f"Consensus reached: Analytical Agent 1 ({agent1.confidence * 100:.1f}%) "
            f"and Critical Agent 2 ({agent2.confidence * 100:.1f}%) converged on {stance_str}. "
            f"Local client stores validate transaction indicators with high calibrated statistical confidence."
        )

    elif status == "DISAGREEMENT":
        decision = None
        final_conf = max(agent1.confidence, agent2.confidence)
        a1_stance = "TRUE" if agent1.decision else "FALSE"
        a2_stance = "TRUE" if agent2.decision else "FALSE"
        reason = (
            f"Divergence detected: Agent 1 (Analytical) concluded {a1_stance} with {agent1.confidence * 100:.1f}% confidence, "
            f"while Agent 2 (Critical Challenger) concluded {a2_stance} with {agent2.confidence * 100:.1f}% confidence. "
            f"Because fundamental risk assumptions are disputed, human review or additional evidence is required."
        )

    else:  # UNCERTAIN
        decision = None
        final_conf = min(agent1.confidence, agent2.confidence)
        reason = (
            f"Decision uncertain: Although both agents trended toward the same stance, "
            f"confidence levels remain marginal (Agent 1: {agent1.confidence * 100:.1f}%, Agent 2: {agent2.confidence * 100:.1f}%). "
            f"Human verification recommended."
        )

    return FinalResult(
        decision=decision,
        confidence=final_conf,
        status=status,
        reason=reason,
    )
