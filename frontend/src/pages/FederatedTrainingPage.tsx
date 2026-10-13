import React from 'react';
import { GitFork, Database, Shield } from 'lucide-react';

export const FederatedTrainingPage: React.FC = () => {
  return (
    <div className="page-container animate-fade-in">
      <div className="page-header">
        <h2>Offline Federated Learning Architecture</h2>
        <p>
          Visualizing the multi-agent decentralized training methodology used to produce the project's fine-tuned LoRA adapters.
        </p>
      </div>

      {/* Visual ASCII / Architecture Diagram */}
      <div className="diagram-card">
        <div style={{ color: 'var(--accent-blue)', fontWeight: 700, marginBottom: '1rem' }}>
          FEDERATED TRAINING TOPOLOGY (OFFLINE SYNCHRONIZATION)
        </div>
        <pre style={{ margin: 0, lineHeight: 1.5 }}>
{`
                  [ FinGPT/fingpt-fiqa_qa ]
                                  │
                 ┌────────────────┴────────────────┐
                 │ (Partitioned Private Data)      │
                 ▼                                 ▼
      [ Agent 1 Private Data ]          [ Agent 2 Private Data ]
           (8,555 rows)                      (8,555 rows)
                 │                                 │
                 ▼                                 ▼
    [ Agent 1 Local Training ]        [ Agent 2 Local Training ]
    Base: Qwen2.5-0.5B-Instruct       Base: Qwen2.5-0.5B-Instruct
    PEFT / LoRA (r=8, alpha=16)       PEFT / LoRA (r=8, alpha=16)
                 │                                 │
                 ▼                                 ▼
    [ qwen/agent1/ ]                  [ qwen/agent2/ ]
    adapter_model.safetensors         adapter_model.safetensors
                 │                                 │
                 └────────────────┬────────────────┘
                                  │
                                  ▼
                         [ FedAvg Aggregator ]
                        Weighted Parameter Merge
                                  │
                                  ▼
                        [ qwen/global_qwen/ ]
                      adapter_model.safetensors
                      (Synchronized Global Model)
`}
        </pre>
      </div>

      {/* Training Specifications */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1.25rem', marginBottom: '2rem' }}>
        <div className="comp-stat-card" style={{ textAlign: 'left' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--accent-indigo)', marginBottom: '0.4rem' }}>
            <Database size={16} />
            <span style={{ fontSize: '0.8rem', fontWeight: 700 }}>Partitioned Dataset</span>
          </div>
          <div style={{ fontSize: '1rem', fontWeight: 700, color: '#fff', marginBottom: '0.2rem' }}>
            FinGPT/fingpt-fiqa_qa
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
            Financial fraud, banking QA & risk instruction tuning. 17,110 total local examples (8,555 allocated privately per agent).
          </div>
        </div>

        <div className="comp-stat-card" style={{ textAlign: 'left' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--accent-blue)', marginBottom: '0.4rem' }}>
            <GitFork size={16} />
            <span style={{ fontSize: '0.8rem', fontWeight: 700 }}>Federated Algorithm</span>
          </div>
          <div style={{ fontSize: '1rem', fontWeight: 700, color: '#fff', marginBottom: '0.2rem' }}>
            Synchronized FedAvg
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
            Synchronized initialization round aggregating local LoRA parameter updates into the Global Qwen adapter.
          </div>
        </div>

        <div className="comp-stat-card" style={{ textAlign: 'left' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--accent-emerald)', marginBottom: '0.4rem' }}>
            <Shield size={16} />
            <span style={{ fontSize: '0.8rem', fontWeight: 700 }}>Privacy Guarantee</span>
          </div>
          <div style={{ fontSize: '1rem', fontWeight: 700, color: '#fff', marginBottom: '0.2rem' }}>
            Zero Raw Data Sharing
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
            Agents only exchange low-rank adapter weight deltas. Raw user prompts and labels remain local.
          </div>
        </div>
      </div>

      {/* Actual Artifacts Table */}
      <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#fff', marginBottom: '0.5rem' }}>
        Trained Artifacts Manifest
      </h3>
      <table className="info-table">
        <thead>
          <tr>
            <th>Component</th>
            <th>Relative Package Path</th>
            <th>Type</th>
            <th>Base Backbone</th>
            <th>Role in System</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Agent 1 Adapter</td>
            <td><span className="code-pill">qwen/agent1/adapter_model.safetensors</span></td>
            <td>LoRA (r=16, α=32)</td>
            <td>Qwen2.5-0.5B-Instruct</td>
            <td>Specialized for analytical and evidence-based assessment</td>
          </tr>
          <tr>
            <td>Agent 2 Adapter</td>
            <td><span className="code-pill">qwen/agent2/adapter_model.safetensors</span></td>
            <td>LoRA (r=16, α=32)</td>
            <td>Qwen2.5-0.5B-Instruct</td>
            <td>Specialized for critical challenging and counterarguments</td>
          </tr>
          <tr>
            <td>Global Qwen Adapter</td>
            <td><span className="code-pill">qwen/global_qwen/adapter_model.safetensors</span></td>
            <td>LoRA (r=16, α=32)</td>
            <td>Qwen2.5-0.5B-Instruct</td>
            <td>FedAvg aggregated synchronized consensus model</td>
          </tr>
        </tbody>
      </table>

      {/* Offline vs Online Note */}
      <div className="uncertainty-note" style={{ marginTop: '2rem', background: 'rgba(99, 102, 241, 0.08)', borderColor: 'var(--border-highlight)', color: '#c7d2fe' }}>
        <span>
          <strong>Operational Distinction:</strong> Federated training is an <em>offline phase</em>. At runtime, the server loads these frozen LoRA weights and performs real-time concurrent multi-agent inference without re-running local gradient updates.
        </span>
      </div>
    </div>
  );
};
