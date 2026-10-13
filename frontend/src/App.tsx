import { useState, useEffect } from 'react';
import { Navbar, type NavTab } from './components/Navbar';
import { ChatPage } from './pages/ChatPage';
import { ArchitecturePage } from './pages/ArchitecturePage';
import { FederatedTrainingPage } from './pages/FederatedTrainingPage';
import { ModelInfoPage } from './pages/ModelInfoPage';
import { ReportModal } from './components/ReportModal';
import { checkBackendHealth } from './api';
import type { ChatResponse } from './types';

export function App() {
  const [currentTab, setCurrentTab] = useState<NavTab>('chat');
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
    setCurrentTab('chat');
    setChatKey((prev) => prev + 1);
    setActiveQuery('');
    setLatestResponse(null);
  };

  const handleOpenReport = () => {
    setIsReportOpen(true);
  };

  return (
    <div className="app-layout" style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      
      {/* Top Navigation Bar */}
      <Navbar
        currentTab={currentTab}
        onSelectTab={(tab) => setCurrentTab(tab)}
        onOpenReport={handleOpenReport}
        onNewChat={handleNewChat}
        backendStatus={backendStatus}
        hasReportData={latestResponse !== null}
      />

      {/* Main Viewport Content based on active tab */}
      <main className="main-chat-viewport" style={{ flex: 1 }}>
        {currentTab === 'chat' && (
          <ChatPage
            key={chatKey}
            onDecisionComplete={handleDecisionComplete}
            onOpenReport={handleOpenReport}
          />
        )}

        {currentTab === 'architecture' && (
          <ArchitecturePage />
        )}

        {currentTab === 'federated' && (
          <FederatedTrainingPage />
        )}

        {currentTab === 'models' && (
          <ModelInfoPage />
        )}
      </main>

      {/* FinCEN SAR & Decision Intelligence Audit Report Modal */}
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
