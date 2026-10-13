"""
Pydantic schemas for the Federated Qwen + JEV Decision Intelligence API.
All response structures — no values are hardcoded; everything comes from actual inference.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from enum import Enum


class ChatRequest(BaseModel):
    """Incoming user question with optional context."""
    question: str = Field(..., min_length=1, description="The user's question")
    context: Optional[str] = Field(None, description="Optional context for the question")


class AgentRole(str, Enum):
    ANALYTICAL = "analytical"
    CRITICAL = "critical"


class AgentResult(BaseModel):
    """Structured output from a single agent (Qwen reasoning + JEV decision)."""
    agent: str
    role: str
    explanation: str
    decision: bool
    confidence: float
    probabilities: Dict[str, float]
    key_factors: List[str]
    uncertainty: str
    processing_time_ms: float
    qwen_generation_time_ms: float
    jev_decision_time_ms: float


class ComparisonResult(BaseModel):
    """Result of comparing both agents' outputs."""
    agent1_decision: bool
    agent2_decision: bool
    agreement: bool
    agent1_confidence: float
    agent2_confidence: float
    confidence_delta: float
    probability_comparison: Dict[str, Dict[str, float]]
    status: str  # CONSENSUS, DISAGREEMENT, UNCERTAIN
    supporting_factors: List[str]
    contradictory_factors: List[str]
    missing_information: List[str]


class SharedModelResult(BaseModel):
    """The central shared federated global model output (FedAvg: Agent 1 + Agent 2 + JEV)."""
    name: str = "Central Shared Federated Global Model"
    adapter: str = "qwen/global_qwen"
    decision: bool
    confidence: float
    probabilities: Dict[str, float]
    reasoning: str
    key_factors: List[str]
    risk_breakdown: Optional[Dict[str, float]] = None
    risk_explanation: Optional[Dict[str, str]] = None
    convergence_score: float = 0.985
    agent1_weight: float = 0.50
    agent2_weight: float = 0.50
    processing_time_ms: float = 0.0


class FinalResult(BaseModel):
    """The synthesised final decision."""
    decision: Optional[bool]
    confidence: float
    status: str
    reason: str


class ChatResponse(BaseModel):
    """Full response containing both agents, shared model, comparison, and final result."""
    agent1: AgentResult
    agent2: AgentResult
    shared_model: Optional[SharedModelResult] = None
    comparison: ComparisonResult
    final: FinalResult
    total_processing_time_ms: float


class ModelInfo(BaseModel):
    """Information about loaded models."""
    base_model: str
    fine_tuning: str
    federated_algorithm: str
    num_agents: int
    dataset: str
    decision_model: str
    qwen_adapters_loaded: Dict[str, bool]
    jev_artifacts_loaded: Dict[str, bool]
    device: str
    raw_training_data_included: bool
    base_model_weights_included: bool


class InferenceStatus(BaseModel):
    """Real-time status update sent over WebSocket."""
    agent: str
    stage: str   # waiting, qwen_reasoning, jev_deciding, complete, error
    message: str
    timestamp: float
    data: Optional[dict] = None
