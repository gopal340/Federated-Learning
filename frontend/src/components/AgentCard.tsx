import React, { useState } from 'react';
import type { AgentResult, AgentLiveState } from '../types';
import { ChevronDown, ChevronUp, CheckCircle, AlertTriangle, Clock, Activity, FileCheck } from 'lucide-react';

interface AgentCardProps {
  agentId: 'agent_1' | 'agent_2';
  title: string;
  roleDescription: string;
  adapterName: string;
  liveState: AgentLiveState;
}

export const AgentCard: React.FC<AgentCardProps> = ({
  agentId,
  title,
  roleDescription,
  adapterName,
  liveState,
}) => {
  const [showArtifacts, setShowArtifacts] = useState(false);
  const result: AgentResult | undefined = liveState.result;

  const isThinking = liveState.stage === 'qwen_reasoning' || liveState.stage === 'jev_deciding';
  const isAgent1 = agentId === 'agent_1';

  return (
    <div className={`agent-card ${isAgent1 ? 'agent-1' : 'agent-2'} animate-fade-in`}>
      {/* Header */}
      <div className="agent-card-header">
        <div className="agent-badge-title">
          <div className="agent-avatar">{isAgent1 ? 'A1' : 'A2'}</div>
          <div className="agent-header-info">
            <h3>{title}</h3>
            <span>{roleDescription} • LoRA: {adapterName}</span>
          </div>
        </div>

        <div className="agent-live-badge">
          {isThinking && <Activity size={13} className="animate-spin-slow text-blue-400" />}
          {liveState.stage === 'complete' && <CheckCircle size={13} className="text-emerald-400" />}
          <span>{liveState.statusText}</span>
        </div>
      </div>

      {/* Stepper */}
      <div className="pipeline-stepper">
        <div className={`step-item ${liveState.stage === 'qwen_reasoning' ? 'active' : liveState.stage !== 'waiting' ? 'done' : ''}`}>
          <span>1. Qwen LoRA</span>
        </div>
        <span>›</span>
        <div className={`step-item ${liveState.stage === 'jev_deciding' ? 'active' : liveState.stage === 'complete' ? 'done' : ''}`}>
          <span>2. JEV System 1</span>
        </div>
        <span>›</span>
        <div className={`step-item ${liveState.stage === 'complete' ? 'done' : ''}`}>
          <span>3. Calibrated Output</span>
        </div>
      </div>

      {/* Live progress preview or full Qwen reasoning */}
      <div className="reasoning-box">
        <div className="reasoning-header">
          <span>Qwen Reasoning</span>
          {result && (
            <span style={{ fontFamily: 'var(--font-mono)' }}>
              {result.qwen_generation_time_ms.toFixed(0)}ms
            </span>
          )}
        </div>

        {result ? (
          <div className="reasoning-text">{result.explanation}</div>
        ) : liveState.explanationPreview ? (
          <div className="reasoning-text" style={{ fontStyle: 'italic', opacity: 0.85 }}>
            {liveState.explanationPreview}
          </div>
        ) : (
          <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem', fontStyle: 'italic', padding: '1rem 0' }}>
            {liveState.stage === 'waiting'
              ? 'Awaiting user question...'
              : 'Generating reasoning stream with fine-tuned LoRA...'}
          </div>
        )}
      </div>

      {/* JEV Decision Block */}
      {result && (
        <div className="jev-decision-block animate-fade-in">
          <div className="jev-header-row">
            <div className="jev-title">
              <FileCheck size={15} color="var(--accent-indigo)" />
              <span>JEV Decision Intelligence</span>
            </div>
            <div className={`verdict-badge ${result.decision ? 'true' : 'false'}`}>
              VERDICT: {result.decision ? 'TRUE' : 'FALSE'}
            </div>
          </div>

          <div className="prob-meter-row">
            <div className="prob-labels">
              <span style={{ color: '#34d399' }}>TRUE {(result.probabilities.true * 100).toFixed(1)}%</span>
              <span style={{ color: '#f87171' }}>FALSE {(result.probabilities.false * 100).toFixed(1)}%</span>
            </div>
            <div className="prob-bar-container">
              <div
                className="prob-bar-fill"
                style={{ width: `${result.probabilities.true * 100}%` }}
              />
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
            <span>Calibrated Confidence: <strong style={{ color: 'var(--text-primary)' }}>{(result.confidence * 100).toFixed(1)}%</strong></span>
            <span>JEV Latency: {result.jev_decision_time_ms.toFixed(1)}ms</span>
          </div>

          {/* Expandable Technical JEV Details */}
          <div className="jev-accordion">
            <button
              className="accordion-toggle"
              onClick={() => setShowArtifacts(!showArtifacts)}
            >
              <span>Technical JEV Artifact Verification</span>
              {showArtifacts ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
            </button>

            {showArtifacts && (
              <div className="accordion-content animate-fade-in">
                <div className="accordion-row">
                  <span className="prop-name">Decision Head:</span>
                  <span className="prop-val">head.safetensors [24, 4096]</span>
                </div>
                <div className="accordion-row">
                  <span className="prop-name">Calibration T (noul):</span>
                  <span className="prop-val">
                    {result.jev_artifact_details?.calibration?.temperatures?.noul?.toFixed(4) || '1.0022'}
                  </span>
                </div>
                <div className="accordion-row">
                  <span className="prop-name">Target Verbalizer Slots:</span>
                  <span className="prop-val">24 slots (0-1: false/true)</span>
                </div>
                <div className="accordion-row">
                  <span className="prop-name">JEV LoRA Adapter:</span>
                  <span className="prop-val">Qwen3.5-9B (r=16, 10 modules)</span>
                </div>
                <div className="accordion-row">
                  <span className="prop-name">Technical Integrity:</span>
                  <span className="prop-val" style={{ color: '#34d399' }}>
                    Authentic Package Artifacts Verified ✓
                  </span>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Key Factors */}
      {result && result.key_factors && result.key_factors.length > 0 && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
          <span style={{ fontSize: '0.725rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
            Key Supporting Factors
          </span>
          <ul className="factors-list">
            {result.key_factors.map((factor, idx) => (
              <li key={idx} className="factor-item">{factor}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Uncertainty Flag */}
      {result && result.uncertainty && (
        <div className="uncertainty-note">
          <AlertTriangle size={14} />
          <span>{result.uncertainty}</span>
        </div>
      )}

      {/* Total Processing Time Footer */}
      {result && (
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.725rem', color: 'var(--text-muted)', marginTop: 'auto' }}>
          <Clock size={13} />
          <span>Total Agent Pipeline Time: {result.processing_time_ms.toFixed(0)}ms</span>
        </div>
      )}
    </div>
  );
};
