"""
Comparison service — synthesizes outputs from Agent 1 (Analytical) and Agent 2 (Critical).

UPGRADE: Transitioned from heuristic confidence penalties to mathematically sound 
Bayesian Updating (Independent Opinion Pooling) to calculate genuine statistical consensus.
"""
import logging
from typing import Dict, List, Optional
from schemas.responses import AgentResult, ComparisonResult, FinalResult

logger = logging.getLogger(__name__)

def calculate_bayesian_consensus(p1: float, p2: float) -> float:
    """
    Applies Bayesian Updating to combine two independent probability estimates.
    Converts probabilities to odds, combines evidence, and returns the joint probability.
    """
    # Clamp to prevent division by zero or absolute certainty (infinity)
    p1 = max(0.001, min(0.999, p1))
    p2 = max(0.001, min(0.999, p2))
    
    # Convert probabilities to Odds (P / 1-P)
    odds1 = p1 / (1.0 - p1)
    odds2 = p2 / (1.0 - p2)
    
    # Combine evidence assuming conditional independence (uninformative prior of 0.5)
    combined_odds = odds1 * odds2
    
    # Convert back to probability
    return combined_odds / (1.0 + combined_odds)

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
    Produce the final synthesized decision using Bayesian probability pooling.
    """
    status = comparison.status

    # Extract the true (fraud) probability from both agents
    p1_true = agent1.probabilities.get("true", agent1.confidence if agent1.decision else 1.0 - agent1.confidence)
    p2_true = agent2.probabilities.get("true", agent2.confidence if agent2.decision else 1.0 - agent2.confidence)
    
    # Calculate mathematically sound joint probability of 'TRUE'
    joint_p_true = calculate_bayesian_consensus(p1_true, p2_true)

    if status == "CONSENSUS":
        decision = agent1.decision
        # Final confidence is the Bayesian probability of the chosen decision
        final_conf = joint_p_true if decision else (1.0 - joint_p_true)
        final_conf = round(final_conf, 4)
        
        stance_str = "AFFIRMATIVE (TRUE — CONFIRMED FRAUD RISK)" if decision else "NEGATIVE (FALSE — BENIGN / AUTHORIZED)"
        reason = (
            f"Consensus reached: Analytical Agent 1 ({agent1.confidence * 100:.1f}%) "
            f"and Critical Agent 2 ({agent2.confidence * 100:.1f}%) converged on {stance_str}. "
            f"Bayesian evidence pooling validates this transaction with a joint statistical consensus of {final_conf * 100:.1f}%."
        )

    elif status == "DISAGREEMENT":
        decision = None
        # In disagreement, Bayesian confidence naturally collapses toward 0.5 (uncertainty)
        final_conf = max(joint_p_true, 1.0 - joint_p_true)
        a1_stance = "TRUE" if agent1.decision else "FALSE"
        a2_stance = "TRUE" if agent2.decision else "FALSE"
        reason = (
            f"Divergence detected: Agent 1 concluded {a1_stance} ({agent1.confidence * 100:.1f}%), "
            f"while Agent 2 concluded {a2_stance} ({agent2.confidence * 100:.1f}%). "
            f"Because fundamental risk assumptions cancel each other out (Joint Probability: {final_conf * 100:.1f}%), "
            f"human review or additional evidence is mathematically required."
        )

    else:  # UNCERTAIN
        decision = None
        final_conf = max(joint_p_true, 1.0 - joint_p_true)
        reason = (
            f"Decision uncertain: Although both agents trended toward the same stance, "
            f"confidence levels remain mathematically marginal (Joint Confidence: {final_conf * 100:.1f}%). "
            f"Human verification recommended."
        )

    return FinalResult(
        decision=decision,
        confidence=final_conf,
        status=status,
        reason=reason,
    )
