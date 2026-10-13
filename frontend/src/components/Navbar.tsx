import React from 'react';
import { Plus, FileText, Activity } from 'lucide-react';

interface NavbarProps {
  onOpenReport: () => void;
  onNewChat: () => void;
  backendStatus: { status: string; models_loaded: boolean; device: string };
  hasReportData: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({
  onOpenReport,
  onNewChat,
  backendStatus,
  hasReportData,
}) => {
  const isOnline = backendStatus.status === 'online' && backendStatus.models_loaded;

  return (
    <header className="header-nav" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0.65rem 1.5rem', background: '#ffffff', borderBottom: '1px solid var(--border-subtle)', position: 'sticky', top: 0, zIndex: 50 }}>
      
      {/* Left: Brand + New Query */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <button 
          className="new-chat-btn" 
          onClick={onNewChat} 
          title="Start New Decision Query"
          style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', padding: '0.4rem 0.85rem', borderRadius: '8px', background: 'var(--bg-tertiary)', border: '1px solid var(--border-subtle)', fontWeight: 600, fontSize: '0.825rem', cursor: 'pointer' }}
        >
          <Plus size={15} />
          <span>New Query</span>
        </button>

        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <div style={{ fontSize: '1rem', fontWeight: 800, color: 'var(--text-primary)', letterSpacing: '-0.02em', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <span>Federated Qwen + JEV</span>
            <span style={{ fontSize: '0.65rem', fontWeight: 700, padding: '0.1rem 0.4rem', background: '#ecfdf5', color: '#047857', borderRadius: '4px', border: '1px solid #a7f3d0' }}>
              V2.0
            </span>
          </div>
          <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
            Decision Intelligence Console
          </span>
        </div>
      </div>

      {/* Right: Hardware Telemetry HUD & Report */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
        
        {/* GPU Telemetry Pill */}
        <div 
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.45rem',
            padding: '0.35rem 0.75rem',
            borderRadius: '9999px',
            background: isOnline ? '#f0fdf4' : '#fef2f2',
            border: `1px solid ${isOnline ? '#bbf7d0' : '#fecaca'}`,
            fontSize: '0.75rem',
            fontWeight: 600,
            color: isOnline ? '#166534' : '#991b1b',
          }}
          title="Runtime Execution Telemetry: NVIDIA GeForce RTX 2050 (4GB VRAM), Qwen Base (~0.9GB), Dynamic LoRA Swapper"
        >
          <Activity size={13} color={isOnline ? '#16a34a' : '#dc2626'} />
          <span>{isOnline ? 'RTX 2050 (CUDA) • 0.9GB VRAM' : 'Engine Offline'}</span>
        </div>

        {/* Report Button */}
        <button
          id="nav-report-btn"
          className={`report-btn ${hasReportData ? 'has-data' : ''}`}
          onClick={onOpenReport}
          title="Open FinCEN SAR & Decision Intelligence Audit Report"
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.45rem',
            padding: '0.4rem 0.9rem',
            borderRadius: '8px',
            background: hasReportData ? 'var(--accent-indigo)' : 'var(--bg-secondary)',
            color: hasReportData ? '#ffffff' : 'var(--text-secondary)',
            border: hasReportData ? 'none' : '1px solid var(--border-subtle)',
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
