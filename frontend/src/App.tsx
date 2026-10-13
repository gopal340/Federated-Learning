import { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { ChatPage } from './pages/ChatPage';
import { ReportModal } from './components/ReportModal';
import { checkBackendHealth } from './api';
import type { ChatResponse } from './types';

export function App() {
  const [chatKey, setChatKey] = useState<number>(0);
  const [activeQuery, setActiveQuery] = useState<string>('');
  const [latestResponse, setLatestResponse] = useState<ChatResponse | null>(null);
  const [isReportOpen, setIsReportOpen] = useState<boolean>(false);

  const [backendStatus, setBackendStatus] = useState({
    status: 'checking',
    models_loaded: false,
    device: 'unknown',
  });

  useEffect(() => {
    async function checkHealth() {
      const status = await checkBackendHealth();
      setBackendStatus(status);
    }
    checkHealth();
    const interval = setInterval(checkHealth, 8000);
    return () => clearInterval(interval);
  }, []);

  const handleDecisionComplete = (query: string, res: ChatResponse) => {
    setActiveQuery(query);
    setLatestResponse(res);
  };

  const handleNewChat = () => {
    setChatKey((prev) => prev + 1);
    setActiveQuery('');
    setLatestResponse(null);
  };

  const handleOpenReport = () => {
    setIsReportOpen(true);
  };

  return (
    <div className="app-layout">
      {/* Top Navbar: ChatGPT minimalist header */}
      <Navbar
        onOpenReport={handleOpenReport}
        onNewChat={handleNewChat}
        backendStatus={backendStatus}
        hasReportData={latestResponse !== null}
      />

      {/* Main Viewport: Pure Chatbot Interface */}
      <main className="main-chat-viewport">
        <ChatPage
          key={chatKey}
          onDecisionComplete={handleDecisionComplete}
          onOpenReport={handleOpenReport}
        />
      </main>

      {/* Decision Intelligence Audit Report Modal */}
      <ReportModal
        isOpen={isReportOpen}
        onClose={() => setIsReportOpen(false)}
        query={activeQuery || 'Latest Decision Intelligence Query'}
        response={latestResponse}
      />
    </div>
  );
}

export default App;
