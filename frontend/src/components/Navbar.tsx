import React from 'react';
import { Plus, FileText } from 'lucide-react';

interface NavbarProps {
  onOpenReport: () => void;
  onNewChat: () => void;
  backendStatus?: { status: string; models_loaded: boolean; device: string };
  hasReportData: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({
  onOpenReport,
  onNewChat,
  hasReportData,
}) => {
  return (
    <header className="header-nav" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0.75rem 1.75rem', background: '#ffffff', borderBottom: '1px solid var(--border-subtle)', position: 'sticky', top: 0, zIndex: 50 }}>
      
      {/* Left: Dark Visible New Chat Button + Brand */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
        <button 
          id="new-chat-btn"
          className="new-chat-btn" 
          onClick={onNewChat} 
          title="Start New Decision Query"
        >
          <Plus size={16} />
          <span>New Chat</span>
        </button>

        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <div style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--text-primary)', letterSpacing: '-0.02em', display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
            <span>Federated Qwen + JEV</span>
            <span style={{ fontSize: '0.65rem', fontWeight: 700, padding: '0.1rem 0.45rem', background: '#ecfdf5', color: '#047857', borderRadius: '4px', border: '1px solid #a7f3d0' }}>
              V2.0
            </span>
          </div>
          <span style={{ fontSize: '0.74rem', color: 'var(--text-muted)' }}>
            Decision Intelligence Console
          </span>
        </div>
      </div>

      {/* Right: SAR Report Action Button */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
        <button
          id="nav-report-btn"
          className={`report-btn ${hasReportData ? 'has-data' : ''}`}
          onClick={onOpenReport}
          title="Open FinCEN SAR & Decision Intelligence Audit Report"
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.45rem',
            padding: '0.45rem 1rem',
            borderRadius: '8px',
            background: hasReportData ? 'var(--accent-indigo)' : '#f8fafc',
            color: hasReportData ? '#ffffff' : '#334155',
            border: hasReportData ? 'none' : '1px solid #cbd5e1',
            fontSize: '0.825rem',
            fontWeight: 600,
            cursor: 'pointer',
            transition: 'all 0.2s',
          }}
        >
          <FileText size={15} />
          <span>SAR Report</span>
          {hasReportData && (
            <span style={{ width: '7px', height: '7px', borderRadius: '50%', background: '#4ade80' }} />
          )}
        </button>
      </div>

    </header>
  );
};
