import React, { useState, useEffect, useRef } from 'react';
import { ArrowUp, Sparkles, AlertCircle, RefreshCw } from 'lucide-react';
import { FederatedSharedCard } from '../components/FederatedSharedCard';
import type { ChatResponse, AgentLiveState } from '../types';
import { sendChatDecision } from '../api';

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  query?: string;
  response?: ChatResponse;
  agent1State?: AgentLiveState;
  agent2State?: AgentLiveState;
  isLoading?: boolean;
  error?: string;
}

interface ChatPageProps {
  onDecisionComplete?: (query: string, res: ChatResponse) => void;
  onOpenReport?: () => void;
}

export const ChatPage: React.FC<ChatPageProps> = ({
  onDecisionComplete,
  onOpenReport,
}) => {
  const [inputQuestion, setInputQuestion] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [elapsedSec, setElapsedSec] = useState<number>(0);

  // Conversation history
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  // Live states for current ongoing inference
  const [agent1Live, setAgent1Live] = useState<AgentLiveState>({
    stage: 'waiting',
    statusText: 'Waiting',
  });
  const [agent2Live, setAgent2Live] = useState<AgentLiveState>({
    stage: 'waiting',
    statusText: 'Waiting',
  });

  const timerRef = useRef<any>(null);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, agent1Live, agent2Live, isLoading]);

  // Clean up timer on unmount
  useEffect(() => {
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, []);

  const handleSend = async (queryText?: string) => {
    const q = (queryText || inputQuestion).trim();
    if (!q || isLoading) return;

    setError(null);
    setIsLoading(true);
    setInputQuestion('');
    setElapsedSec(0);

    const userMsgId = 'user_' + Date.now();
    const assistantMsgId = 'asst_' + Date.now();

    const initialA1State: AgentLiveState = {
      stage: 'qwen_reasoning',
      statusText: 'Analyzing evidence with qwen/agent1 LoRA...',
    };
    const initialA2State: AgentLiveState = {
      stage: 'qwen_reasoning',
      statusText: 'Evaluating critical challenges with qwen/agent2 LoRA...',
    };

    setAgent1Live(initialA1State);
    setAgent2Live(initialA2State);

    // Append user message & assistant thinking message
    setMessages((prev) => [
      ...prev,
      { id: userMsgId, role: 'user', query: q },
      {
        id: assistantMsgId,
        role: 'assistant',
        isLoading: true,
        agent1State: initialA1State,
        agent2State: initialA2State,
      },
    ]);

    // Animated deliberation stage tracker
    let sec = 0;
    if (timerRef.current) clearInterval(timerRef.current);
    timerRef.current = setInterval(() => {
      sec += 1;
      setElapsedSec(sec);

      if (sec === 4) {
        setAgent1Live({
          stage: 'qwen_reasoning',
          statusText: 'Qwen LoRA: Generating analytical explanation (qwen/agent1)...',
        });
      } else if (sec === 10) {
        setAgent2Live({
          stage: 'qwen_reasoning',
          statusText: 'Qwen LoRA: Analyzing counterarguments & risks (qwen/agent2)...',
        });
      } else if (sec >= 18) {
        setAgent1Live((prev) => ({
          ...prev,
          stage: 'jev_deciding',
          statusText: 'JEV Engine: Computing calibrated decision-head projection...',
        }));
        setAgent2Live((prev) => ({
          ...prev,
          stage: 'jev_deciding',
          statusText: 'JEV Engine: Applying System 1 calibration & slots...',
        }));
      }
    }, 1000);

    try {
      const res = await sendChatDecision(q);

      if (timerRef.current) clearInterval(timerRef.current);

      const finalA1State: AgentLiveState = {
        stage: 'complete',
        statusText: `Verdict: ${res.agent1.decision ? 'True' : 'False'} (${(res.agent1.confidence * 100).toFixed(0)}%)`,
      };
      const finalA2State: AgentLiveState = {
        stage: 'complete',
        statusText: `Verdict: ${res.agent2.decision ? 'True' : 'False'} (${(res.agent2.confidence * 100).toFixed(0)}%)`,
      };

      setAgent1Live(finalA1State);
      setAgent2Live(finalA2State);

      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === assistantMsgId
            ? {
                ...msg,
                response: res,
                isLoading: false,
                agent1State: finalA1State,
                agent2State: finalA2State,
              }
            : msg
        )
      );

      // Notify parent App for Report availability
      if (onDecisionComplete) {
        onDecisionComplete(q, res);
      }
    } catch (err: any) {
      if (timerRef.current) clearInterval(timerRef.current);
      const errMsg = err.message || 'Inference execution failed';
      setError(errMsg);

      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === assistantMsgId
            ? {
                ...msg,
                isLoading: false,
                error: errMsg,
              }
            : msg
        )
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      {/* Messages Viewport */}
      <div className="chat-messages-area">
        {messages.length === 0 ? (
          /* Clean Minimalist Welcome State without hardcoded prompt buttons */
          <div className="chat-welcome-state animate-fade-in" style={{ padding: '3rem 1.5rem', textAlign: 'center' }}>
            <div className="welcome-avatar" style={{ margin: '0 auto 1.25rem', width: '56px', height: '56px', borderRadius: '16px', background: '#ecfdf5', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Sparkles size={28} color="#10a37f" />
            </div>
            <h2 style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '0.5rem', letterSpacing: '-0.02em' }}>
              Federated Multi-Agent Decision Console
            </h2>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', maxWidth: '560px', margin: '0 auto', lineHeight: 1.6 }}>
              Type any financial transaction scenario, account query, or risk investigation into the input bar below to initiate real-time dual-agent deliberation.
            </p>
          </div>
        ) : (
          /* Conversation message stream */
          <div className="message-stream">
            {messages.map((msg) => {
              if (msg.role === 'user') {
                return (
                  <div key={msg.id} className="chat-bubble-row user-row animate-fade-in">
                    <div className="chat-bubble user-bubble">
                      <div className="bubble-text">{msg.query}</div>
                    </div>
                  </div>
                );
              }

              // Assistant message
              return (
                <div key={msg.id} className="chat-bubble-row assistant-row animate-fade-in">
                  <div className="assistant-content-wrapper">
                    {/* Live deliberation stages during execution */}
                    {msg.isLoading && (
                      <div className="deliberation-banner animate-fade-in">
                        <div className="deliberation-header">
                          <div className="deliberation-pulse">
                            <span className="pulse-dot" />
                            <span className="pulse-text">Dual-Agent Deliberation in Progress...</span>
                          </div>
                          <span className="deliberation-timer">{elapsedSec}s elapsed</span>
                        </div>

                        <div className="deliberation-nodes-grid">
                          <div className="deliberation-node-card">
                            <div className="node-card-title">
                              <span className="node-badge agent1-badge">Agent 1: Fraud Specialist</span>
                            </div>
                            <div className="node-card-status">
                              <RefreshCw size={13} className="animate-spin-slow" />
                              <span>{msg.agent1State?.statusText || agent1Live.statusText}</span>
                            </div>
                          </div>

                          <div className="deliberation-node-card">
                            <div className="node-card-title">
                              <span className="node-badge agent2-badge">Agent 2: AML Challenger</span>
                            </div>
                            <div className="node-card-status">
                              <RefreshCw size={13} className="animate-spin-slow" />
                              <span>{msg.agent2State?.statusText || agent2Live.statusText}</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Final decision response card */}
                    {msg.response && (
                      <FederatedSharedCard
                        agent1={msg.response.agent1}
                        agent2={msg.response.agent2}
                        sharedModel={msg.response.shared_model}
                        comparison={msg.response.comparison}
                        final={msg.response.final}
                        totalTimeMs={msg.response.total_processing_time_ms}
                        onOpenReport={onOpenReport}
                      />
                    )}

                    {/* Error message inside card if any */}
                    {msg.error && (
                      <div className="chat-error-banner animate-fade-in" style={{ marginTop: '0.85rem' }}>
                        <AlertCircle size={16} />
                        <span>{msg.error}</span>
                      </div>
                    )}
                  </div>
                </div>
              );
            })}

            {error && (
              <div className="chat-error-banner animate-fade-in">
                <AlertCircle size={16} />
                <span>{error}</span>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Clean Bottom Input Area */}
      <div className="chat-bottom-dock">
        {/* Input capsule */}
        <div className="dock-input-capsule">
          <input
            id="chat-question-input"
            type="text"
            className="dock-text-input"
            placeholder="Type your scenario or decision query here (e.g. 'Account balance drained after sudden international wire...')..."
            value={inputQuestion}
            onChange={(e) => setInputQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            disabled={isLoading}
          />

          <button
            id="chat-send-btn"
            className={`dock-send-btn ${inputQuestion.trim() && !isLoading ? 'active' : ''}`}
            onClick={() => handleSend()}
            disabled={isLoading || !inputQuestion.trim()}
            title="Send query"
          >
            {isLoading ? <RefreshCw size={16} className="animate-spin-slow" /> : <ArrowUp size={18} />}
          </button>
        </div>

        <div className="dock-footer-note">
          Federated Qwen LoRA multi-agent deliberation + JEV-9B calibrated decision intelligence.
        </div>
      </div>
    </div>
  );
};
