import React from 'react';
import type { ComparisonResult, FinalResult, AgentResult } from '../types';
import { CheckCircle2, AlertOctagon, HelpCircle, FileText } from 'lucide-react';

interface ComparisonCardProps {
  comparison: ComparisonResult;
  final: FinalResult;
  agent1: AgentResult;
  agent2: AgentResult;
  totalTimeMs: number;
  onOpenReport?: () => void;
}

export const ComparisonCard: React.FC<ComparisonCardProps> = ({
  comparison,
  final,
  agent1,
  agent2,
  totalTimeMs,
  onOpenReport,
}) => {
  const isConsensus = comparison.status === 'CONSENSUS';
  const isDisagreement = comparison.status === 'DISAGREEMENT';

  const statusClass = isConsensus
    ? 'status-consensus'
    : isDisagreement
    ? 'status-disagreement'
    : 'status-uncertain';

  return (
    <div className="comparison-container animate-fade-in">
      {/* Status Banner */}
      <div className={`comparison-status-banner ${statusClass}`}>
        <div className="comparison-status-title">
          {isConsensus && <CheckCircle2 size={24} />}
          {isDisagreement && <AlertOctagon size={24} />}
          {!isConsensus && !isDisagreement && <HelpCircle size={24} />}
          <span>
            {isConsensus && 'CONSENSUS REACHED'}
            {isDisagreement && 'AGENT DISAGREEMENT DETECTED'}
            {!isConsensus && !isDisagreement && 'DECISION UNCERTAIN'}
          </span>
        </div>

        <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.85rem' }}>
          Pipeline Latency: {totalTimeMs.toFixed(0)}ms
        </div>
      </div>

      {/* Stats Grid */}
      <div className="comparison-stats-grid">
        <div className="comp-stat-card">
          <div className="comp-stat-label">Agent 1 (Analytical)</div>
          <div className="comp-stat-value" style={{ color: agent1.decision ? '#34d399' : '#f87171' }}>
            {agent1.decision ? 'TRUE' : 'FALSE'}
            <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginLeft: '0.4rem' }}>
              ({(agent1.confidence * 100).toFixed(1)}%)
            </span>
          </div>
        </div>

        <div className="comp-stat-card">
          <div className="comp-stat-label">Agent 2 (Critical)</div>
          <div className="comp-stat-value" style={{ color: agent2.decision ? '#34d399' : '#f87171' }}>
            {agent2.decision ? 'TRUE' : 'FALSE'}
            <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginLeft: '0.4rem' }}>
              ({(agent2.confidence * 100).toFixed(1)}%)
            </span>
          </div>
        </div>

        <div className="comp-stat-card">
          <div className="comp-stat-label">Final Synthesized Decision</div>
          <div className="comp-stat-value" style={{ color: final.decision === null ? '#fbbf24' : final.decision ? '#34d399' : '#f87171' }}>
            {final.decision === null ? 'UNCERTAIN' : final.decision ? 'PROCEED (TRUE)' : 'HALT (FALSE)'}
            <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginLeft: '0.4rem' }}>
              ({(final.confidence * 100).toFixed(1)}%)
            </span>
          </div>
        </div>
      </div>

      {/* Synthesis Reason Box */}
      <div style={{ marginBottom: '1.5rem' }}>
        <h3 style={{ fontSize: '0.85rem', textTransform: 'uppercase', color: 'var(--text-muted)', marginBottom: '0.5rem', fontWeight: 600 }}>
          Synthesis & Recommendation
        </h3>
        <div className="synthesis-box">
          {final.reason}
        </div>
      </div>

      {/* Probability Comparison Matrix */}
      <div style={{ marginBottom: '1.5rem' }}>
        <h3 style={{ fontSize: '0.85rem', textTransform: 'uppercase', color: 'var(--text-muted)', marginBottom: '0.5rem', fontWeight: 600 }}>
          Calibrated Probability Matrix
        </h3>
        <table className="info-table" style={{ marginTop: 0 }}>
          <thead>
            <tr>
              <th>Proposition Stance</th>
              <th>Agent 1 (qwen/agent1 + JEV)</th>
              <th>Agent 2 (qwen/agent2 + JEV)</th>
              <th>Delta</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <span className="code-pill" style={{ color: '#34d399' }}>TRUE (Affirmative)</span>
              </td>
              <td style={{ fontFamily: 'var(--font-mono)' }}>{(agent1.probabilities.true * 100).toFixed(2)}%</td>
              <td style={{ fontFamily: 'var(--font-mono)' }}>{(agent2.probabilities.true * 100).toFixed(2)}%</td>
              <td style={{ fontFamily: 'var(--font-mono)' }}>
                {Math.abs((agent1.probabilities.true - agent2.probabilities.true) * 100).toFixed(2)}%
              </td>
            </tr>
            <tr>
              <td>
                <span className="code-pill" style={{ color: '#f87171' }}>FALSE (Negative)</span>
              </td>
              <td style={{ fontFamily: 'var(--font-mono)' }}>{(agent1.probabilities.false * 100).toFixed(2)}%</td>
              <td style={{ fontFamily: 'var(--font-mono)' }}>{(agent2.probabilities.false * 100).toFixed(2)}%</td>
              <td style={{ fontFamily: 'var(--font-mono)' }}>
                {Math.abs((agent1.probabilities.false - agent2.probabilities.false) * 100).toFixed(2)}%
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Supporting vs Contradictory Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
        <div>
          <h4 style={{ fontSize: '0.8rem', color: '#34d399', marginBottom: '0.5rem', fontWeight: 700 }}>
            Supporting Signals
          </h4>
          <ul className="factors-list">
            {comparison.supporting_factors.length > 0 ? (
              comparison.supporting_factors.map((f, i) => (
                <li key={i} className="factor-item">{f}</li>
              ))
            ) : (
              <li className="factor-item" style={{ color: 'var(--text-muted)' }}>None flagged</li>
            )}
          </ul>
        </div>

        <div>
          <h4 style={{ fontSize: '0.8rem', color: '#f87171', marginBottom: '0.5rem', fontWeight: 700 }}>
            Risk & Challenge Factors
          </h4>
          <ul className="factors-list">
            {comparison.contradictory_factors.length > 0 ? (
              comparison.contradictory_factors.map((f, i) => (
                <li key={i} className="factor-item">{f}</li>
              ))
            ) : (
              <li className="factor-item" style={{ color: 'var(--text-muted)' }}>None flagged</li>
            )}
          </ul>
        </div>
      </div>

      {/* Report Button Row */}
      {onOpenReport && (
        <div className="card-report-action-row">
          <button className="card-report-btn" onClick={onOpenReport}>
            <FileText size={16} />
            <span>Generate & View Full Decision Audit Report</span>
          </button>
        </div>
      )}
    </div>
  );
};
