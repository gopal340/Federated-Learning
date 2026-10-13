export interface JevArtifactDetails {
  model_name: string;
  architecture: string;
  base_model_dependency: string;
  required_vram_bf16: string;
  head_safetensors: {
    verified: boolean;
    weight_shape: number[];
    bias_shape: number[];
    in_features: number;
    out_features: number;
  };
  calibration: {
    verified: boolean;
    temperatures: {
      noul: number;
      choice: number;
      score: number;
    };
    source_checkpoint: string;
  };
  slots: {
    num_slots: number;
    ranges: Record<string, [number, number]>;
    verbalizers: string[];
    verbalizer_ids: number[];
  };
  adapter: {
    verified: boolean;
    rank: number;
    target_modules: string[];
    base_model_class: string;
  };
  remote_endpoint: string;
}

export interface AgentResult {
  agent: string;
  role: 'analytical' | 'critical' | string;
  explanation: string;
  decision: boolean;
  confidence: number;
  probabilities: {
    true: number;
    false: number;
  };
  key_factors: string[];
  uncertainty: string;
  processing_time_ms: number;
  qwen_generation_time_ms: number;
  jev_decision_time_ms: number;
  jev_artifact_details?: JevArtifactDetails;
}

export interface ComparisonResult {
  agent1_decision: boolean;
  agent2_decision: boolean;
  agreement: boolean;
  agent1_confidence: number;
  agent2_confidence: number;
  confidence_delta: number;
  probability_comparison: {
    true: { agent_1: number; agent_2: number };
    false: { agent_1: number; agent_2: number };
  };
  status: 'CONSENSUS' | 'DISAGREEMENT' | 'UNCERTAIN';
  supporting_factors: string[];
  contradictory_factors: string[];
  missing_information: string[];
}

export interface SharedModelResult {
  name: string;
  adapter: string;
  decision: boolean;
  confidence: number;
  probabilities: {
    true: number;
    false: number;
  };
  reasoning: string;
  key_factors: string[];
  risk_breakdown?: Record<string, number>;
  risk_explanation?: Record<string, string>;
  convergence_score: number;
  agent1_weight: number;
  agent2_weight: number;
  processing_time_ms: number;
}

export interface FinalResult {
  decision: boolean | null;
  confidence: number;
  status: 'CONSENSUS' | 'DISAGREEMENT' | 'UNCERTAIN';
  reason: string;
}

export interface ChatResponse {
  agent1: AgentResult;
  agent2: AgentResult;
  shared_model?: SharedModelResult;
  comparison: ComparisonResult;
  final: FinalResult;
  total_processing_time_ms: number;
}

export interface ModelInfo {
  base_model: string;
  fine_tuning: string;
  federated_algorithm: string;
  num_agents: number;
  dataset: string;
  decision_model: string;
  qwen_adapters_loaded: Record<string, boolean>;
  jev_artifacts: JevArtifactDetails;
  device: string;
  raw_training_data_included: boolean;
  base_model_weights_included: boolean;
}

export type AgentStage = 'waiting' | 'qwen_reasoning' | 'qwen_complete' | 'jev_deciding' | 'complete' | 'error';

export interface AgentLiveState {
  stage: AgentStage;
  statusText: string;
  explanationPreview?: string;
  result?: AgentResult;
}
