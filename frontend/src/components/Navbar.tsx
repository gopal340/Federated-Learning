import React from 'react';
import { Plus, FileText } from 'lucide-react';

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
    <header className="header-nav">
      <div className="header-left">
        <button className="new-chat-btn" onClick={onNewChat} title="Start New Decision Query">
          <Plus size={16} />
          <span>New Chat</span>
        </button>

        <div className="brand-title-group">
          <h1>Federated Qwen + JEV</h1>
          <span className="brand-subtitle">Multi-Agent Decision Intelligence</span>
        </div>
      </div>

      <div className="header-right">
        {/* Status indicator */}
        <div className={`status-pill ${isOnline ? 'online' : 'offline'}`} title={`Device: ${backendStatus.device}`}>
          <span className="status-dot" />
          <span>
            {isOnline
              ? `Models Active (${backendStatus.device.toUpperCase()})`
              : backendStatus.status === 'online'
              ? 'Loading Models...'
              : 'Engine Offline'}
          </span>
        </div>

        {/* Prominent Report Button */}
        <button
          id="nav-report-btn"
          className={`report-btn ${hasReportData ? 'has-data' : ''}`}
          onClick={onOpenReport}
          title="Open Decision Intelligence Audit Report"
        >
          <FileText size={16} />
          <span>Report</span>
          {hasReportData && <span className="report-indicator-dot" />}
        </button>
      </div>
    </header>
  );
};
