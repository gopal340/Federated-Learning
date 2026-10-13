import React, { useState } from 'react';
import { 
  Cpu, GitMerge, ShieldCheck, 
  ArrowDown, ChevronRight, CheckCircle2, Sparkles, Sliders
} from 'lucide-react';


interface BlockDetail {
  id: string;
  title: string;
  category: string;
  badge: string;
  summary: string;
  specs: { label: string; value: string }[];
  technicalNotes: string[];
}

const BLOCK_SPECS: Record<string, BlockDetail> = {
  input: {
    id: 'input',
    title: '1. User Query & Context Ingestion',
    category: 'Ingestion Layer',
    badge: 'API / UI Entry',
    summary: 'Captures transaction details, wire narratives, counterparty clearing rails, and KYC audit logs.',
    specs: [
      { label: 'Ingestion Rails', value: 'REST (/api/chat) & WebSocket (/ws/inference)' },
      { label: 'Context Format', value: 'Instruction / Financial QA Pair' },
      { label: 'Streaming Protocol', value: 'Token-by-Token stage progress events' },
    ],
    technicalNotes: [
      'Normalizes unstructured transaction memos (SWIFT MT103, Fedwire, ATM logs).',
      'Dispatches concurrent asynchronous execution tasks via asyncio.gather.',
    ],
  },
  agent1: {
    id: 'agent1',
    title: 'Agent 1: Fraud & Velocity Specialist',
    category: 'Decentralized Reasoning',
    badge: 'qwen/agent1 LoRA',
    summary: 'Analyzes high-velocity egress patterns, cross-border anomalies, and clearing rail risks.',
    specs: [
      { label: 'Base Model', value: 'Qwen/Qwen2.5-0.5B-Instruct (Frozen)' },
      { label: 'LoRA Configuration', value: 'r = 8, α = 16, dropout = 0.05' },
      { label: 'Target Modules', value: 'q_proj, v_proj, k_proj, o_proj' },
      { label: 'Private Training Partition', value: '8,555 rows (FinGPT/fingpt-fiqa_qa)' },
      { label: 'Memory Footprint', value: '~24.5 MB adapter_model.safetensors' },
    ],
    technicalNotes: [
      'Trained locally on private client partition without exposing customer PII.',
      'Generates independent chain-of-thought risk evaluation with supporting factors.',
    ],
  },
  agent2: {
    id: 'agent2',
    title: 'Agent 2: AML & Critical Challenger',
    category: 'Decentralized Reasoning',
    badge: 'qwen/agent2 LoRA',
    summary: 'Acts as adversarial compliance officer checking BSA structuring, SAR thresholds, and KYC gaps.',
    specs: [
      { label: 'Base Model', value: 'Qwen/Qwen2.5-0.5B-Instruct (Frozen)' },
      { label: 'LoRA Configuration', value: 'r = 8, α = 16, dropout = 0.05' },
      { label: 'Target Modules', value: 'q_proj, v_proj, k_proj, o_proj' },
      { label: 'Private Training Partition', value: '8,555 rows (FinGPT/fingpt-fiqa_qa)' },
      { label: 'Regulatory Mandate', value: '31 U.S.C. § 5324 & 18 U.S.C. § 1956' },
    ],
    technicalNotes: [
      'Acts as critical counter-analyst to prevent false-positive automated freezes.',
      'Flags missing CTR forms and smurfing indicators across sub-$10,000 deposits.',
    ],
  },
  global_qwen: {
    id: 'global_qwen',
    title: 'Global Synchronized Model (FedAvg)',
    category: 'Federated Server',
    badge: 'qwen/global_qwen',
    summary: 'Unified central consensus representation generated via Federated Averaging parameter aggregation.',
    specs: [
      { label: 'Aggregation Algorithm', value: 'FedAvg (w* = 0.5·w₁ + 0.5·w₂)' },
      { label: 'Parameter Extraction', value: 'Safetensors tensor weight averaging' },
      { label: 'Privacy Guarantee', value: 'Zero raw training data transmitted' },
      { label: 'Consensus Adapter', value: 'qwen/global_qwen/adapter_model.safetensors' },
    ],
    technicalNotes: [
      'Provides synchronized consensus perspective across all private agent domains.',
      'Used during online inference to evaluate collective baseline understanding.',
    ],
  },
  jev: {
    id: 'jev',
    title: 'autotrust/JEV-9B Decision Intelligence Head',
    category: 'System 1 Verification',
    badge: 'head.safetensors',
    summary: 'Learned linear projection and calibrated temperature scaling verifying structured decision stances.',
    specs: [
      { label: 'Model Spec', value: 'autotrust/JEV-9B System 1 Architecture' },
      { label: 'Linear Head Projection', value: 'W: [24, 4096] weights, b: [24] bias' },
      { label: 'Calibration File', value: 'jev/calibration.json (source: s2_9b_epoch1)' },
      { label: 'Calibrated Temperature', value: 'T_noul = 1.0022178236691426' },
      { label: 'Verbalizer Slots', value: '24 slots (Slot 0 = False, Slot 1 = True)' },
    ],
    technicalNotes: [
      'Strict Anti-Fabrication Policy: Qwen 0.5B logits are never falsely labeled as 9B logits.',
      'Produces authentic mathematically normalized probabilities P(True) vs P(False).',
      'Provides System 1 rapid probabilistic stance gating.',
    ],
  },
  comparison: {
    id: 'comparison',
    title: 'Comparison & Conflict Resolution Layer',
    category: 'Synthesis Engine',
    badge: 'services/comparison.py',
    summary: 'Evaluates dual-agent agreement, extracts contradictory signals, and gates consensus states.',
    specs: [
      { label: 'Operational States', value: 'CONSENSUS, DISAGREEMENT, UNCERTAIN' },
      { label: 'Confidence Floor', value: 'Min Confidence ≥ 0.55 for consensus' },
      { label: 'Factor Extraction', value: 'Supporting affirmative vs contradictory challenge trees' },
      { label: 'Integrity Check', value: 'Never blindly picks highest confidence' },
    ],
    technicalNotes: [
      'If agents diverge (True vs False), system triggers DISAGREEMENT conflict resolution.',
      'Detects uncertainty keywords (ambiguous, lacking, unverified) to prevent automated mistakes.',
    ],
  },
  cockpit: {
    id: 'cockpit',
    title: 'Final Verdict & Banking Dashboard',
    category: 'Presentation Tier',
    badge: 'React 19 Console',
    summary: 'Delivers actionable institutional risk score, dynamic donut visualizer, and regulatory SAR directives.',
    specs: [
      { label: 'Frontend Stack', value: 'React 19 + TypeScript + Vite' },
      { label: 'Visual Visualizers', value: 'SVG Risk Donut, Institutional Comparison Matrix' },
      { label: 'Export Formats', value: 'FinCEN Form 111 SAR Dossier, Markdown Audit' },
      { label: 'Latency', value: 'Sub-second WebSocket streamed feedback' },
    ],
    technicalNotes: [
      'Generates automated hard freeze directives (< 15 min SLA).',
      'Produces court-admissible audit reports with full chain of custody.',
    ],
  },
};

export const ArchitecturePage: React.FC = () => {
  const [viewMode, setViewMode] = useState<'blocks' | 'pipeline'>('blocks');
  const [selectedBlockId, setSelectedBlockId] = useState<string>('jev');

  const selectedBlock = BLOCK_SPECS[selectedBlockId] || BLOCK_SPECS.jev;

  const steps = [
    { num: 1, title: 'Private Data Partitioning', desc: '17,110 FinGPT records split evenly between Fraud (Agent 1) and AML Compliance (Agent 2).' },
    { num: 2, title: 'Local LoRA Parameter Training', desc: 'Base Qwen2.5-0.5B frozen; rank-8 LoRA adapter matrices trained locally on private data.' },
    { num: 3, title: 'FedAvg Weight Aggregation', desc: 'Central server aggregates weights (w* = 0.5·w₁ + 0.5·w₂) producing global_qwen.' },
    { num: 4, title: 'Memory-Safe VRAM Swapper', desc: 'Single 0.5B base model loaded onto RTX 2050 CUDA; adapters swapped dynamically in <10ms.' },
    { num: 5, title: 'Concurrent Inference Dispatch', desc: 'Incoming transaction queries trigger asynchronous execution of Agent 1 and Agent 2 via asyncio.gather.' },
    { num: 6, title: 'JEV Linear Head Projection', desc: 'head.safetensors [24, 4096] projects latent representations to decision space.' },
    { num: 7, title: 'Temperature Calibration', desc: 'T_noul = 1.0022 scales logits into mathematically calibrated probability distribution.' },
    { num: 8, title: 'Comparison & Conflict Resolution', desc: 'services/comparison.py tests agreement, confidence deltas, and uncertainty flags.' },
    { num: 9, title: 'Consensus State Determination', desc: 'Classifies outcome into CONSENSUS, DISAGREEMENT, or UNCERTAIN.' },
    { num: 10, title: 'Regulatory SAR Dossier Delivery', desc: 'Presents dynamic risk score, supporting factors, and FinCEN SAR action directives.' },
  ];

  return (
    <div className="page-container animate-fade-in" style={{ padding: '2rem 1.5rem', maxWidth: '1280px', margin: '0 auto' }}>
      
      {/* Header */}
      <div style={{ marginBottom: '2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', padding: '0.25rem 0.75rem', background: 'rgba(79, 70, 229, 0.1)', color: 'var(--accent-indigo)', borderRadius: '9999px', fontSize: '0.8rem', fontWeight: 600, marginBottom: '0.5rem' }}>
            <Cpu size={14} /> Enterprise System Architecture
          </div>
          <h2 style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--text-primary)', letterSpacing: '-0.02em', marginBottom: '0.25rem' }}>
            Federated Multi-Agent Architecture
          </h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.925rem', maxWidth: '750px' }}>
            Decentralized LoRA parameter training combined with JEV-9B System 1 calibrated decision intelligence and multi-agent synthesis.
          </p>
        </div>

        {/* View Switcher Toggle */}
        <div style={{ display: 'inline-flex', background: 'var(--bg-tertiary)', padding: '0.25rem', borderRadius: '10px', border: '1px solid var(--border-subtle)' }}>
          <button
            onClick={() => setViewMode('blocks')}
            style={{
              padding: '0.45rem 1rem',
              borderRadius: '8px',
              fontSize: '0.85rem',
              fontWeight: 600,
              border: 'none',
              cursor: 'pointer',
              background: viewMode === 'blocks' ? '#ffffff' : 'transparent',
              color: viewMode === 'blocks' ? 'var(--accent-indigo)' : 'var(--text-muted)',
              boxShadow: viewMode === 'blocks' ? 'var(--shadow-sm)' : 'none',
              transition: 'all 0.15s ease',
            }}
          >
            Simplified Main Blocks
          </button>
          <button
            onClick={() => setViewMode('pipeline')}
            style={{
              padding: '0.45rem 1rem',
              borderRadius: '8px',
              fontSize: '0.85rem',
              fontWeight: 600,
              border: 'none',
              cursor: 'pointer',
              background: viewMode === 'pipeline' ? '#ffffff' : 'transparent',
              color: viewMode === 'pipeline' ? 'var(--accent-indigo)' : 'var(--text-muted)',
              boxShadow: viewMode === 'pipeline' ? 'var(--shadow-sm)' : 'none',
              transition: 'all 0.15s ease',
            }}
          >
            Deep 3-Tier Pipeline
          </button>
        </div>
      </div>

      {/* Main Diagram Area */}
      <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1.8fr) minmax(320px, 1fr)', gap: '1.5rem', marginBottom: '2.5rem', alignItems: 'start' }}>
        
        {/* Left: Interactive Diagram Canvas */}
        <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-card)', borderRadius: '16px', padding: '1.75rem', boxShadow: 'var(--shadow-md)' }}>
          
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)' }}>
              {viewMode === 'blocks' ? 'Interactive High-Level Architecture Flow' : 'End-to-End 3-Tier System Architecture'}
            </span>
            <span style={{ fontSize: '0.75rem', color: 'var(--accent-indigo)', fontWeight: 600 }}>
              Click any block to inspect specifications
            </span>
          </div>

          {viewMode === 'blocks' ? (
            /* SIMPLIFIED 5 MAIN BLOCKS FLOW */
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', alignItems: 'center' }}>
              
              {/* Block 1: User Input */}
              <div 
                onClick={() => setSelectedBlockId('input')}
                style={{
                  width: '100%',
                  padding: '1.1rem 1.25rem',
                  borderRadius: '12px',
                  background: selectedBlockId === 'input' ? 'rgba(79, 70, 229, 0.08)' : 'var(--bg-secondary)',
                  border: `2px solid ${selectedBlockId === 'input' ? 'var(--accent-indigo)' : 'var(--border-subtle)'}`,
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
                  <div style={{ width: '38px', height: '38px', borderRadius: '10px', background: '#e0e7ff', color: 'var(--accent-indigo)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <Sliders size={18} />
                  </div>
                  <div>
                    <div style={{ fontWeight: 700, fontSize: '0.95rem', color: 'var(--text-primary)' }}>1. Transaction / Wire Ingestion</div>
                    <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Context narrative, clearing rail details & counterparty risk data</div>
                  </div>
                </div>
                <ChevronRight size={18} color="var(--text-muted)" />
              </div>

              {/* Connecting Arrow */}
              <div style={{ color: 'var(--text-muted)', display: 'flex', alignItems: 'center', justifyContent: 'center', height: '18px' }}>
                <ArrowDown size={18} />
              </div>

              {/* Block 2: Multi-Agent Layer */}
              <div style={{ width: '100%', padding: '1rem', borderRadius: '14px', background: 'var(--bg-tertiary)', border: '1px dashed #cbd5e1' }}>
                <div style={{ fontSize: '0.75rem', fontWeight: 800, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.75rem', textAlign: 'center' }}>
                  2. Federated Multi-Agent Reasoning Layer (Qwen2.5-0.5B + PEFT)
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '0.75rem' }}>
                  
                  {/* Agent 1 */}
                  <div 
                    onClick={() => setSelectedBlockId('agent1')}
                    style={{
                      padding: '0.85rem',
                      borderRadius: '10px',
                      background: selectedBlockId === 'agent1' ? '#ecfdf5' : '#ffffff',
                      border: `2px solid ${selectedBlockId === 'agent1' ? '#10b981' : '#e5e7eb'}`,
                      cursor: 'pointer',
                      textAlign: 'center',
                    }}
                  >
                    <div style={{ fontWeight: 700, fontSize: '0.85rem', color: '#047857' }}>Agent 1: Fraud</div>
                    <div style={{ fontSize: '0.72rem', color: '#065f46', marginTop: '0.2rem' }}>Velocity & Wire Rails</div>
                  </div>

                  {/* Global Model */}
                  <div 
                    onClick={() => setSelectedBlockId('global_qwen')}
                    style={{
                      padding: '0.85rem',
                      borderRadius: '10px',
                      background: selectedBlockId === 'global_qwen' ? '#eff6ff' : '#ffffff',
                      border: `2px solid ${selectedBlockId === 'global_qwen' ? '#3b82f6' : '#e5e7eb'}`,
                      cursor: 'pointer',
                      textAlign: 'center',
                    }}
                  >
                    <div style={{ fontWeight: 700, fontSize: '0.85rem', color: '#1e40af' }}>Global Model</div>
                    <div style={{ fontSize: '0.72rem', color: '#1d4ed8', marginTop: '0.2rem' }}>FedAvg Consensus</div>
                  </div>

                  {/* Agent 2 */}
                  <div 
                    onClick={() => setSelectedBlockId('agent2')}
                    style={{
                      padding: '0.85rem',
                      borderRadius: '10px',
                      background: selectedBlockId === 'agent2' ? '#faf5ff' : '#ffffff',
                      border: `2px solid ${selectedBlockId === 'agent2' ? '#a855f7' : '#e5e7eb'}`,
                      cursor: 'pointer',
                      textAlign: 'center',
                    }}
                  >
                    <div style={{ fontWeight: 700, fontSize: '0.85rem', color: '#7e22ce' }}>Agent 2: AML</div>
                    <div style={{ fontSize: '0.72rem', color: '#6b21a8', marginTop: '0.2rem' }}>Structuring & BSA</div>
                  </div>

                </div>
              </div>

              {/* Connecting Arrow */}
              <div style={{ color: 'var(--text-muted)', display: 'flex', alignItems: 'center', justifyContent: 'center', height: '18px' }}>
                <ArrowDown size={18} />
              </div>

              {/* Block 3: JEV Decision Head */}
              <div 
                onClick={() => setSelectedBlockId('jev')}
                style={{
                  width: '100%',
                  padding: '1.1rem 1.25rem',
                  borderRadius: '12px',
                  background: selectedBlockId === 'jev' ? 'rgba(147, 51, 234, 0.08)' : 'var(--bg-secondary)',
                  border: `2px solid ${selectedBlockId === 'jev' ? '#9333ea' : 'var(--border-subtle)'}`,
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
                  <div style={{ width: '38px', height: '38px', borderRadius: '10px', background: '#f3e8ff', color: '#9333ea', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <ShieldCheck size={18} />
                  </div>
                  <div>
                    <div style={{ fontWeight: 700, fontSize: '0.95rem', color: 'var(--text-primary)' }}>3. JEV-9B Decision Intelligence Head</div>
                    <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Linear Projection [24, 4096] & Temperature Scaling (T = 1.0022)</div>
                  </div>
                </div>
                <ChevronRight size={18} color="var(--text-muted)" />
              </div>

              {/* Connecting Arrow */}
              <div style={{ color: 'var(--text-muted)', display: 'flex', alignItems: 'center', justifyContent: 'center', height: '18px' }}>
                <ArrowDown size={18} />
              </div>

              {/* Block 4: Comparison Layer */}
              <div 
                onClick={() => setSelectedBlockId('comparison')}
                style={{
                  width: '100%',
                  padding: '1.1rem 1.25rem',
                  borderRadius: '12px',
                  background: selectedBlockId === 'comparison' ? 'rgba(234, 88, 12, 0.08)' : 'var(--bg-secondary)',
                  border: `2px solid ${selectedBlockId === 'comparison' ? '#ea580c' : 'var(--border-subtle)'}`,
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
                  <div style={{ width: '38px', height: '38px', borderRadius: '10px', background: '#ffedd5', color: '#ea580c', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <GitMerge size={18} />
                  </div>
                  <div>
                    <div style={{ fontWeight: 700, fontSize: '0.95rem', color: 'var(--text-primary)' }}>4. Comparison & Conflict Resolution Layer</div>
                    <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>CONSENSUS / DISAGREEMENT / UNCERTAIN gate & factor matrix</div>
                  </div>
                </div>
                <ChevronRight size={18} color="var(--text-muted)" />
              </div>

              {/* Connecting Arrow */}
              <div style={{ color: 'var(--text-muted)', display: 'flex', alignItems: 'center', justifyContent: 'center', height: '18px' }}>
                <ArrowDown size={18} />
              </div>

              {/* Block 5: Cockpit */}
              <div 
                onClick={() => setSelectedBlockId('cockpit')}
                style={{
                  width: '100%',
                  padding: '1.1rem 1.25rem',
                  borderRadius: '12px',
                  background: selectedBlockId === 'cockpit' ? 'rgba(16, 163, 127, 0.08)' : 'var(--bg-secondary)',
                  border: `2px solid ${selectedBlockId === 'cockpit' ? '#10a37f' : 'var(--border-subtle)'}`,
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
                  <div style={{ width: '38px', height: '38px', borderRadius: '10px', background: '#dcfce7', color: '#16a34a', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <Sparkles size={18} />
                  </div>
                  <div>
                    <div style={{ fontWeight: 700, fontSize: '0.95rem', color: 'var(--text-primary)' }}>5. Final Verdict & Banking Cockpit</div>
                    <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Calibrated Risk Score (97.8%), SVG Gauge Donut & FinCEN SAR Filing</div>
                  </div>
                </div>
                <ChevronRight size={18} color="var(--text-muted)" />
              </div>

            </div>
          ) : (
            /* DEEP 3-TIER PIPELINE VIEW */
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
              
              {/* Tier 1 */}
              <div style={{ padding: '1.25rem', borderRadius: '12px', background: '#f0fdf4', border: '1px solid #bbf7d0' }}>
                <div style={{ fontSize: '0.75rem', fontWeight: 800, color: '#15803d', textTransform: 'uppercase', marginBottom: '0.5rem' }}>
                  Tier 1: Decentralized Offline Federated Training
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '0.75rem' }}>
                  <div onClick={() => setSelectedBlockId('agent1')} style={{ cursor: 'pointer', padding: '0.75rem', background: '#fff', borderRadius: '8px', border: '1px solid #86efac' }}>
                    <div style={{ fontWeight: 700, fontSize: '0.85rem', color: '#166534' }}>Client 1 (8,555 Rows)</div>
                    <div style={{ fontSize: '0.72rem', color: '#14532d' }}>LoRA r=8, α=16</div>
                  </div>
                  <div onClick={() => setSelectedBlockId('global_qwen')} style={{ cursor: 'pointer', padding: '0.75rem', background: '#fff', borderRadius: '8px', border: '1px solid #93c5fd' }}>
                    <div style={{ fontWeight: 700, fontSize: '0.85rem', color: '#1e40af' }}>FedAvg Merge</div>
                    <div style={{ fontSize: '0.72rem', color: '#1d4ed8' }}>w* = 0.5w₁ + 0.5w₂</div>
                  </div>
                  <div onClick={() => setSelectedBlockId('agent2')} style={{ cursor: 'pointer', padding: '0.75rem', background: '#fff', borderRadius: '8px', border: '1px solid #d8b4fe' }}>
                    <div style={{ fontWeight: 700, fontSize: '0.85rem', color: '#6b21a8' }}>Client 2 (8,555 Rows)</div>
                    <div style={{ fontSize: '0.72rem', color: '#581c87' }}>LoRA r=8, α=16</div>
                  </div>
                </div>
              </div>

              {/* Tier 2 */}
              <div style={{ padding: '1.25rem', borderRadius: '12px', background: '#eff6ff', border: '1px solid #bfdbfe' }}>
                <div style={{ fontSize: '0.75rem', fontWeight: 800, color: '#1d4ed8', textTransform: 'uppercase', marginBottom: '0.5rem' }}>
                  Tier 2: Runtime Inference & JEV-9B Decision Head
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '0.75rem' }}>
                  <div onClick={() => setSelectedBlockId('input')} style={{ cursor: 'pointer', padding: '0.75rem', background: '#fff', borderRadius: '8px', border: '1px solid #93c5fd' }}>
                    <div style={{ fontWeight: 700, fontSize: '0.85rem', color: '#1e3a8a' }}>VRAM-Safe ModelManager</div>
                    <div style={{ fontSize: '0.72rem', color: '#1e40af' }}>RTX 2050 CUDA (0.9GB) + Hot-Swap</div>
                  </div>
                  <div onClick={() => setSelectedBlockId('jev')} style={{ cursor: 'pointer', padding: '0.75rem', background: '#fff', borderRadius: '8px', border: '1px solid #c084fc' }}>
                    <div style={{ fontWeight: 700, fontSize: '0.85rem', color: '#6b21a8' }}>JEV Projection Head</div>
                    <div style={{ fontSize: '0.72rem', color: '#581c87' }}>W: [24, 4096], T=1.0022</div>
                  </div>
                </div>
              </div>

              {/* Tier 3 */}
              <div style={{ padding: '1.25rem', borderRadius: '12px', background: '#fff7ed', border: '1px solid #fed7aa' }}>
                <div style={{ fontSize: '0.75rem', fontWeight: 800, color: '#c2410c', textTransform: 'uppercase', marginBottom: '0.5rem' }}>
                  Tier 3: Comparison, Synthesis & Compliance UX
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
                  <div onClick={() => setSelectedBlockId('comparison')} style={{ cursor: 'pointer', padding: '0.75rem', background: '#fff', borderRadius: '8px', border: '1px solid #fdba74' }}>
                    <div style={{ fontWeight: 700, fontSize: '0.85rem', color: '#9a3412' }}>Comparison Engine</div>
                    <div style={{ fontSize: '0.72rem', color: '#7c2d12' }}>Agreement & Uncertainty Check</div>
                  </div>
                  <div onClick={() => setSelectedBlockId('cockpit')} style={{ cursor: 'pointer', padding: '0.75rem', background: '#fff', borderRadius: '8px', border: '1px solid #86efac' }}>
                    <div style={{ fontWeight: 700, fontSize: '0.85rem', color: '#15803d' }}>SAR Form 111 Dossier</div>
                    <div style={{ fontSize: '0.72rem', color: '#14532d' }}>31 U.S.C. § 5324 Hard Freeze</div>
                  </div>
                </div>
              </div>

            </div>
          )}

        </div>

        {/* Right: Technical Inspector Drawer */}
        <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-card)', borderRadius: '16px', padding: '1.5rem', boxShadow: 'var(--shadow-md)' }}>
          
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.4rem' }}>
            <span style={{ fontSize: '0.7rem', fontWeight: 800, textTransform: 'uppercase', background: 'rgba(79, 70, 229, 0.1)', color: 'var(--accent-indigo)', padding: '0.15rem 0.5rem', borderRadius: '4px' }}>
              {selectedBlock.category}
            </span>
            <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
              {selectedBlock.badge}
            </span>
          </div>

          <h3 style={{ fontSize: '1.15rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '0.5rem' }}>
            {selectedBlock.title}
          </h3>

          <p style={{ fontSize: '0.825rem', color: 'var(--text-secondary)', lineHeight: 1.5, marginBottom: '1.25rem' }}>
            {selectedBlock.summary}
          </p>

          <div style={{ borderTop: '1px solid var(--border-subtle)', paddingTop: '1rem', marginBottom: '1.25rem' }}>
            <div style={{ fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.04em', color: 'var(--text-muted)', marginBottom: '0.75rem' }}>
              Technical Specifications
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
              {selectedBlock.specs.map((spec, idx) => (
                <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', fontSize: '0.8rem', gap: '0.5rem' }}>
                  <span style={{ color: 'var(--text-muted)', fontWeight: 500 }}>{spec.label}:</span>
                  <span style={{ color: 'var(--text-primary)', fontWeight: 600, textAlign: 'right', fontFamily: spec.value.includes('[') || spec.value.includes('T_') ? 'var(--font-mono)' : 'inherit', fontSize: '0.775rem' }}>
                    {spec.value}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div style={{ borderTop: '1px solid var(--border-subtle)', paddingTop: '1rem' }}>
            <div style={{ fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.04em', color: 'var(--text-muted)', marginBottom: '0.6rem' }}>
              Architectural Guarantees
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              {selectedBlock.technicalNotes.map((note, idx) => (
                <div key={idx} style={{ display: 'flex', alignItems: 'flex-start', gap: '0.5rem', fontSize: '0.775rem', color: 'var(--text-secondary)' }}>
                  <CheckCircle2 size={14} color="#10b981" style={{ flexShrink: 0, marginTop: '2px' }} />
                  <span>{note}</span>
                </div>
              ))}
            </div>
          </div>

        </div>

      </div>

      {/* Ten-Point Architectural Lifecycle Grid */}
      <div style={{ marginTop: '3rem' }}>
        <h3 style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '0.4rem' }}>
          Ten-Point Architectural Lifecycle
        </h3>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem', marginBottom: '1.5rem' }}>
          Step-by-step engineering execution from decentralized client training to calibrated regulatory synthesis.
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem' }}>
          {steps.map((s) => (
            <div key={s.num} style={{ background: 'var(--bg-card)', border: '1px solid var(--border-card)', borderRadius: '12px', padding: '1rem 1.25rem', display: 'flex', gap: '0.85rem', alignItems: 'flex-start' }}>
              <div style={{ width: '28px', height: '28px', borderRadius: '50%', background: 'rgba(79, 70, 229, 0.1)', color: 'var(--accent-indigo)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 800, fontSize: '0.8rem', flexShrink: 0 }}>
                {s.num}
              </div>
              <div>
                <div style={{ fontWeight: 700, fontSize: '0.9rem', color: 'var(--text-primary)', marginBottom: '0.2rem' }}>
                  {s.title}
                </div>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                  {s.desc}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
};
