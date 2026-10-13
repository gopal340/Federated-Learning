import React from 'react';
import { Database, Shield, GitMerge, CheckCircle, ArrowDown, Lock } from 'lucide-react';

export const FederatedTrainingPage: React.FC = () => {
  return (
    <div className="page-container animate-fade-in" style={{ padding: '2rem 1.5rem', maxWidth: '1200px', margin: '0 auto' }}>
      
      {/* Header */}
      <div style={{ marginBottom: '2rem' }}>
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', padding: '0.25rem 0.75rem', background: 'rgba(16, 163, 127, 0.1)', color: 'var(--accent-emerald)', borderRadius: '9999px', fontSize: '0.8rem', fontWeight: 600, marginBottom: '0.5rem' }}>
          <Shield size={14} /> Decentralized Privacy-Preserving Machine Learning
        </div>
        <h2 style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--text-primary)', letterSpacing: '-0.02em', marginBottom: '0.25rem' }}>
          Offline Federated Training Architecture
        </h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.925rem', maxWidth: '750px' }}>
          Multi-agent decentralized training methodology combining local parameter isolation with synchronized FedAvg aggregation.
        </p>
      </div>

      {/* Visual Federated Topology Diagram */}
      <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-card)', borderRadius: '16px', padding: '2rem', boxShadow: 'var(--shadow-md)', marginBottom: '2.5rem' }}>
        <div style={{ fontSize: '0.8rem', fontWeight: 800, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '1.5rem', textAlign: 'center' }}>
          Federated LoRA Parameter Synchronization Topology
        </div>

        {/* Top: Central Partitioned Dataset */}
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginBottom: '1.5rem' }}>
          <div style={{ padding: '1rem 1.75rem', background: 'var(--bg-secondary)', border: '1px solid var(--border-subtle)', borderRadius: '12px', textAlign: 'center', maxWidth: '420px', width: '100%' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem', color: 'var(--accent-indigo)', fontWeight: 700, fontSize: '0.95rem', marginBottom: '0.2rem' }}>
              <Database size={16} />
              <span>FinGPT/fingpt-fiqa_qa Benchmark</span>
            </div>
            <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
              17,110 Financial QA Pairs Partitioned 50 / 50 into Decentralized Client Silos
            </div>
          </div>
          <ArrowDown size={20} color="var(--text-muted)" style={{ marginTop: '0.5rem' }} />
        </div>

        {/* Middle: Decentralized Client Nodes (Agent 1 & Agent 2) */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.5rem', marginBottom: '1.5rem' }}>
          
          {/* Client Node 1 */}
          <div style={{ padding: '1.25rem', background: '#f0fdf4', border: '1.5px solid #86efac', borderRadius: '14px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
              <div style={{ fontWeight: 800, fontSize: '0.95rem', color: '#166534' }}>Client Node 1 (Agent 1)</div>
              <span style={{ fontSize: '0.7rem', fontWeight: 700, background: '#dcfce7', color: '#15803d', padding: '0.15rem 0.5rem', borderRadius: '4px' }}>Private Partition</span>
            </div>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.8rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: '#14532d' }}>
                <span>Private Training Data:</span>
                <span style={{ fontWeight: 700 }}>8,555 Financial Fraud Rows</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: '#14532d' }}>
                <span>Domain Specialization:</span>
                <span style={{ fontWeight: 700 }}>Velocity & Rail Egress Anomaly</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: '#14532d' }}>
                <span>Base Model:</span>
                <span style={{ fontWeight: 700 }}>Qwen2.5-0.5B-Instruct (Frozen)</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: '#14532d' }}>
                <span>PEFT Method:</span>
                <span style={{ fontWeight: 700 }}>LoRA (r=8, α=16, modules: q,v,k,o)</span>
              </div>
              <div style={{ marginTop: '0.5rem', padding: '0.5rem', background: '#ffffff', borderRadius: '6px', border: '1px solid #bbf7d0', fontSize: '0.75rem', color: '#166534', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                <Lock size={12} />
                <span>Zero customer data leaves the local node</span>
              </div>
            </div>
          </div>

          {/* Client Node 2 */}
          <div style={{ padding: '1.25rem', background: '#faf5ff', border: '1.5px solid #d8b4fe', borderRadius: '14px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
              <div style={{ fontWeight: 800, fontSize: '0.95rem', color: '#6b21a8' }}>Client Node 2 (Agent 2)</div>
              <span style={{ fontSize: '0.7rem', fontWeight: 700, background: '#f3e8ff', color: '#7e22ce', padding: '0.15rem 0.5rem', borderRadius: '4px' }}>Private Partition</span>
            </div>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.8rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: '#581c87' }}>
                <span>Private Training Data:</span>
                <span style={{ fontWeight: 700 }}>8,555 AML & Risk Rows</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: '#581c87' }}>
                <span>Domain Specialization:</span>
                <span style={{ fontWeight: 700 }}>Structuring (31 U.S.C. § 5324) & BSA</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: '#581c87' }}>
                <span>Base Model:</span>
                <span style={{ fontWeight: 700 }}>Qwen2.5-0.5B-Instruct (Frozen)</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: '#581c87' }}>
                <span>PEFT Method:</span>
                <span style={{ fontWeight: 700 }}>LoRA (r=8, α=16, modules: q,v,k,o)</span>
              </div>
              <div style={{ marginTop: '0.5rem', padding: '0.5rem', background: '#ffffff', borderRadius: '6px', border: '1px solid #e9d5ff', fontSize: '0.75rem', color: '#6b21a8', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                <Lock size={12} />
                <span>Zero customer data leaves the local node</span>
              </div>
            </div>
          </div>

        </div>

        {/* Bottom: FedAvg Parameter Aggregator */}
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <ArrowDown size={20} color="var(--text-muted)" style={{ marginBottom: '0.5rem' }} />
          <div style={{ padding: '1.25rem 2rem', background: '#eff6ff', border: '1.5px solid #93c5fd', borderRadius: '14px', textAlign: 'center', maxWidth: '580px', width: '100%' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem', color: '#1e40af', fontWeight: 800, fontSize: '1rem', marginBottom: '0.35rem' }}>
              <GitMerge size={18} />
              <span>FedAvg Parameter Aggregator (Federated Server)</span>
            </div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.85rem', color: '#1d4ed8', fontWeight: 700, margin: '0.4rem 0' }}>
              w* = 0.5 · w₁ + 0.5 · w₂
            </div>
            <div style={{ fontSize: '0.78rem', color: '#1e3a8a', lineHeight: 1.5 }}>
              Averages adapter tensor weights directly without accessing raw training data, producing the synchronized global consensus model (<code>qwen/global_qwen</code>).
            </div>
          </div>
        </div>

      </div>

      {/* 3 Core Federated Guarantees */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.25rem' }}>
        <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-card)', borderRadius: '12px', padding: '1.25rem' }}>
          <div style={{ color: '#10b981', fontWeight: 700, fontSize: '0.95rem', marginBottom: '0.4rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <CheckCircle size={16} /> Privacy-First Architecture
          </div>
          <p style={{ fontSize: '0.825rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
            Client transaction records, financial histories, and PII are never transferred to external servers. Only low-rank mathematical delta weights (24 MB safetensors) participate in aggregation.
          </p>
        </div>

        <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-card)', borderRadius: '12px', padding: '1.25rem' }}>
          <div style={{ color: '#3b82f6', fontWeight: 700, fontSize: '0.95rem', marginBottom: '0.4rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <CheckCircle size={16} /> Synchronized Global Consensus
          </div>
          <p style={{ fontSize: '0.825rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
            The global consensus model combines the fraud detection acumen of Agent 1 with the regulatory compliance scrutiny of Agent 2, preventing institutional blind spots.
          </p>
        </div>

        <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-card)', borderRadius: '12px', padding: '1.25rem' }}>
          <div style={{ color: '#8b5cf6', fontWeight: 700, fontSize: '0.95rem', marginBottom: '0.4rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <CheckCircle size={16} /> Single Base Model Swapping
          </div>
          <p style={{ fontSize: '0.825rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
            Runs comfortably on standard 4GB VRAM hardware (NVIDIA RTX 2050) by keeping base model weights static in memory and swapping lightweight LoRA adapters in under 10ms.
          </p>
        </div>
      </div>

    </div>
  );
};
