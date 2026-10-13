import React, { useState, useEffect, useRef } from 'react';
import { ArrowUp, Sparkles, AlertCircle, User, Bot, RefreshCw } from 'lucide-react';
import { FederatedSharedCard } from '../components/FederatedSharedCard';
import type { ChatResponse, AgentLiveState } from '../types';
import { sendChatDecision } from '../api';

const DEMO_PROMPTS = [
  {
    title: 'Wire Velocity Fraud',
    desc: 'Rapid international transfer check',
    text: 'Does this series of multiple international wire transfers with rapid velocity require fraud investigation?',
  },
  {
    title: 'AML Structuring',
    desc: 'Sub-threshold cash deposits',
    text: 'An account received five $9,950 cash deposits across different ATM branches within 48 hours. Does this indicate structuring under BSA/AML regulations?',
  },
  {
    title: 'Card & Identity Theft',
    desc: 'Impossible travel card activity',
    text: 'A debit transaction of $3,500 was initiated in Tokyo 20 minutes after an in-person chip transaction in Chicago. Should this transaction be blocked?',
  },
];

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
          statusText: 'JEV Engine: Applying calibration temperature (T=1.0022)...',
        }));
      }
    }, 1000);

    try {
      // Execute robust HTTP POST to backend
      const res = await sendChatDecision(q);

      if (timerRef.current) clearInterval(timerRef.current);

      const finalA1State: AgentLiveState = {
        stage: 'complete',
        statusText: 'Complete',
        result: res.agent1,
      };
      const finalA2State: AgentLiveState = {
        stage: 'complete',
        statusText: 'Complete',
        result: res.agent2,
      };

      setAgent1Live(finalA1State);
      setAgent2Live(finalA2State);

      // Update message with complete deliberation result
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
          /* Empty state: ChatGPT style */
          <div className="chat-welcome-state animate-fade-in">
            <div className="welcome-avatar">
              <Sparkles size={28} color="#10a37f" />
            </div>
            <h2>What decision would you like to evaluate?</h2>
            <p>
              Dual-agent federated deliberation powered by trained Qwen LoRA adapters and verified JEV Decision Intelligence.
            </p>

            <div className="welcome-prompts-grid">
              {DEMO_PROMPTS.map((p, idx) => (
                <button
                  key={idx}
                  className="welcome-prompt-card"
                  onClick={() => handleSend(p.text)}
                  disabled={isLoading}
                >
                  <div className="prompt-title">{p.title}</div>
                  <div className="prompt-desc">{p.desc}</div>
                </button>
              ))}
            </div>
          </div>
        ) : (
          /* Conversation message stream */
          <div className="message-stream">
            {messages.map((msg) => {
              if (msg.role === 'user') {
                return (
                  <div key={msg.id} className="message-row user-row animate-fade-in">
                    <div className="message-content user-bubble">
                      <p>{msg.query}</p>
                    </div>
                    <div className="avatar-icon user-avatar">
                      <User size={16} />
                    </div>
                  </div>
                );
              }

              // Assistant message
              const a1State = msg.isLoading ? agent1Live : (msg.agent1State || agent1Live);
              const a2State = msg.isLoading ? agent2Live : (msg.agent2State || agent2Live);

              return (
                <div key={msg.id} className="message-row assistant-row animate-fade-in">
                  <div className="avatar-icon bot-avatar">
                    <Bot size={18} />
                  </div>
                  <div className="message-content assistant-content">
                    {/* Header badge */}
                    <div className="assistant-header-meta">
                      <span className="badge-tag">FEDERATED DELIBERATION</span>
                      {msg.isLoading ? (
                        <span className="badge-time" style={{ color: '#10a37f', fontWeight: 600 }}>
                          Deliberating ({elapsedSec}s)...
                        </span>
                      ) : msg.response ? (
                        <span className="badge-time">
                          Latency: {msg.response.total_processing_time_ms.toFixed(0)}ms
                        </span>
                      ) : null}
                    </div>

                    {/* Live Deliberation in progress */}
                    {msg.isLoading && (
                      <div className="live-deliberating-box animate-fade-in">
                        <div className="live-node-progress-row">
                          <div className="live-node-pill">
                            <span className="live-pulse-dot"></span>
                            <span>Node 1 (Analytical): {a1State.statusText}</span>
                          </div>
                          <div className="live-node-pill">
                            <span className="live-pulse-dot"></span>
                            <span>Node 2 (Challenger): {a2State.statusText}</span>
                          </div>
                        </div>
                        <div className="live-progress-bar-container">
                          <div className="live-progress-bar-fill"></div>
                        </div>
                      </div>
                    )}

                    {/* Complete Federated Deliberation Topology & Shared Master Model */}
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

      {/* Fixed Bottom Input Area like ChatGPT */}
      <div className="chat-bottom-dock">
        {/* Quick prompt suggestions when not empty */}
        {messages.length > 0 && (
          <div className="dock-suggestions-row">
            {DEMO_PROMPTS.map((p, idx) => (
              <button
                key={idx}
                className="dock-suggestion-chip"
                onClick={() => handleSend(p.text)}
                disabled={isLoading}
              >
                <span>{p.title}</span>
              </button>
            ))}
          </div>
        )}

        {/* Input capsule */}
        <div className="dock-input-capsule">
          <input
            id="chat-question-input"
            type="text"
            className="dock-text-input"
            placeholder="Ask a decision query (e.g. 'Should this transaction be flagged for fraud?')..."
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
