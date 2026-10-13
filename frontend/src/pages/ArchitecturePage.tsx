import React from 'react';

export const ArchitecturePage: React.FC = () => {
  const steps = [
    {
      num: 1,
      title: 'Agent 1 Local Training',
      desc: 'Trained locally on private partition of FinGPT/fingpt-fiqa_qa (8,555 rows) with fraud detection & transaction focus.',
    },
    {
      num: 2,
      title: 'Agent 2 Local Training',
      desc: 'Trained locally on independent private partition (8,555 rows) with critical challenger persona.',
    },
    {
      num: 3,
      title: 'LoRA Parameter Extraction',
      desc: 'Rank-16 low-rank adapter matrices extracted from self-attention and MLP projections without altering base weights.',
    },
    {
      num: 4,
      title: 'Federated Averaging (FedAvg)',
      desc: 'Synchronized aggregation of Agent 1 and Agent 2 LoRA weights into unified global representation.',
    },
    {
      num: 5,
      title: 'Global Qwen Synchronized Model',
      desc: 'Produces the synchronized global adapter (qwen/global_qwen) representing decentralized collective knowledge.',
    },
    {
      num: 6,
      title: 'Qwen Natural-Language Reasoning',
      desc: 'Incoming user questions are processed concurrently by both agents using their respective fine-tuned LoRA adapters.',
    },
    {
      num: 7,
      title: 'JEV-9B System 1 Decision Head',
      desc: 'The trained 24-slot decision head (head.safetensors) and per-kind temperature calibration (calibration.json) verify structured decisions.',
    },
    {
      num: 8,
      title: 'Concurrent Multi-Agent Execution',
      desc: 'Both agents generate independent reasoning streams concurrently via asyncio.gather without seeing each other\'s output.',
    },
    {
      num: 9,
      title: 'Comparison & Conflict Layer',
      desc: 'Evaluates agreement, confidence delta, contradictory signals, and uncertainty indicators. Never blindly picks highest confidence.',
    },
    {
      num: 10,
      title: 'Final Decision & Synthesis',
      desc: 'Synthesizes findings into CONSENSUS, DISAGREEMENT, or UNCERTAIN with human-readable rationale.',
    },
  ];

  return (
    <div className="page-container animate-fade-in">
      <div className="page-header">
        <h2>System Architecture & Inference Flow</h2>
        <p>
          End-to-end pipeline connecting offline federated parameter synchronization to real-time multi-agent structured decision intelligence.
        </p>
      </div>

      {/* Online Inference Topology Diagram */}
      <div className="diagram-card">
        <div style={{ color: 'var(--accent-indigo)', fontWeight: 700, marginBottom: '1rem' }}>
          ONLINE INFERENCE TOPOLOGY (CONCURRENT MULTI-AGENT REASONING)
        </div>
        <pre style={{ margin: 0, lineHeight: 1.5 }}>
{`
                               [ USER QUERY ]
                                      │
                   ┌──────────────────┴──────────────────┐
                   │                                     │
                   ▼                                     ▼
        [ AGENT 1: ANALYTICAL ]               [ AGENT 2: CRITICAL ]
        Adapter: qwen/agent1                  Adapter: qwen/agent2
                   │                                     │
                   ▼                                     ▼
           Qwen Reasoning                        Qwen Reasoning
       (Evidence & Risk Signals)             (Assumptions & Challenges)
                   │                                     │
                   ▼                                     ▼
           JEV Decision Head                     JEV Decision Head
          (head.safetensors)                    (head.safetensors)
                   │                                     │
                   ▼                                     ▼
        Structured Probability                Structured Probability
           P(True) / P(False)                    P(True) / P(False)
                   │                                     │
                   └──────────────────┬──────────────────┘
                                      │
                                      ▼
                           [ COMPARISON LAYER ]
                   Agreement • Conflict • Uncertainty
                                      │
                                      ▼
                          [ FINAL SYNTHESIS RESULT ]
                     CONSENSUS / DISAGREEMENT / UNCERTAIN
`}
        </pre>
      </div>

      {/* 10 Step Architecture Breakdown */}
      <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#fff', marginBottom: '1rem' }}>
        Ten-Point Architectural Lifecycle
      </h3>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1rem' }}>
        {steps.map((s) => (
          <div key={s.num} className="comp-stat-card" style={{ textAlign: 'left', display: 'flex', gap: '0.85rem' }}>
            <div style={{
              width: '28px',
              height: '28px',
              borderRadius: '50%',
              background: 'rgba(99, 102, 241, 0.2)',
              color: 'var(--accent-indigo)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontWeight: 800,
              fontSize: '0.8rem',
              flexShrink: 0,
            }}>
              {s.num}
            </div>
            <div>
              <div style={{ fontWeight: 700, fontSize: '0.9rem', color: '#fff', marginBottom: '0.2rem' }}>
                {s.title}
              </div>
              <div style={{ fontSize: '0.775rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                {s.desc}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
