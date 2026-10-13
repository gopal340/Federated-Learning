import React, { useState, useEffect, useRef } from 'react';
import { ArrowUp, Sparkles, AlertCircle, RefreshCw, Sliders, ChevronDown, ChevronUp, Send } from 'lucide-react';
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

  // Scenario Builder state
  const [showBuilder, setShowBuilder] = useState(false);
  const [builderAmount, setBuilderAmount] = useState('9,950');
  const [builderRail, setBuilderRail] = useState('SWIFT MT103 (Cross-Border Wire)');
  const [builderVelocity, setBuilderVelocity] = useState('4 transactions within 12 hours');
  const [builderJurisdiction, setBuilderJurisdiction] = useState('Offshore Jurisdiction (Cayman Islands)');
  const [builderProfile, setBuilderProfile] = useState('Newly opened account with zero prior history');

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

  const handleBuildScenario = () => {
    const text = `A customer initiated ${builderVelocity} totaling $${builderAmount} each via ${builderRail} directed to ${builderJurisdiction}. Customer profile: ${builderProfile}. Does this require immediate hard hold and FinCEN SAR filing under BSA anti-structuring regulations?`;
    setShowBuilder(false);
    handleSend(text);
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

            {/* Scenario Builder Toggle */}
            <div style={{ maxWidth: '640px', width: '100%', margin: '0 auto 1.5rem', textAlign: 'left' }}>
              <div 
                onClick={() => setShowBuilder(!showBuilder)}
                style={{
                  padding: '0.75rem 1rem',
                  borderRadius: '10px',
                  background: 'var(--bg-card)',
                  border: '1.5px solid var(--border-subtle)',
                  cursor: 'pointer',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  boxShadow: 'var(--shadow-sm)',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontWeight: 700, fontSize: '0.85rem', color: 'var(--accent-indigo)' }}>
                  <Sliders size={15} />
                  <span>Interactive Scenario Builder (Custom Parameters)</span>
                </div>
                {showBuilder ? <ChevronUp size={16} color="var(--text-muted)" /> : <ChevronDown size={16} color="var(--text-muted)" />}
              </div>

              {showBuilder && (
                <div style={{ marginTop: '0.5rem', padding: '1.25rem', background: '#f8fafc', border: '1px solid var(--border-subtle)', borderRadius: '12px' }} className="animate-fade-in">
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.85rem', marginBottom: '1rem', fontSize: '0.8rem' }}>
                    <div>
                      <label style={{ display: 'block', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>Transaction Amount ($)</label>
                      <input 
                        type="text" 
                        value={builderAmount} 
                        onChange={(e) => setBuilderAmount(e.target.value)}
                        style={{ width: '100%', padding: '0.4rem 0.6rem', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '0.825rem' }} 
                      />
                    </div>
                    <div>
                      <label style={{ display: 'block', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>Clearing Rail</label>
                      <select 
                        value={builderRail} 
                        onChange={(e) => setBuilderRail(e.target.value)}
                        style={{ width: '100%', padding: '0.4rem 0.6rem', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '0.825rem', background: '#fff' }}
                      >
                        <option>SWIFT MT103 (Cross-Border Wire)</option>
                        <option>Fedwire (High-Value Domestic)</option>
                        <option>ACH Batch Payment</option>
                        <option>ATM Multiple Cash Rail</option>
                      </select>
                    </div>
                    <div>
                      <label style={{ display: 'block', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>Velocity Pattern</label>
                      <select 
                        value={builderVelocity} 
                        onChange={(e) => setBuilderVelocity(e.target.value)}
                        style={{ width: '100%', padding: '0.4rem 0.6rem', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '0.825rem', background: '#fff' }}
                      >
                        <option>4 transactions within 12 hours</option>
                        <option>5 consecutive deposits within 48 hours</option>
                        <option>Single rapid egress transfer</option>
                      </select>
                    </div>
                    <div>
                      <label style={{ display: 'block', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>Destination Territory</label>
                      <select 
                        value={builderJurisdiction} 
                        onChange={(e) => setBuilderJurisdiction(e.target.value)}
                        style={{ width: '100%', padding: '0.4rem 0.6rem', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '0.825rem', background: '#fff' }}
                      >
                        <option>Offshore Jurisdiction (Cayman Islands)</option>
                        <option>European Private Bank (Switzerland)</option>
                        <option>Domestic Clearing Account (USA)</option>
                      </select>
                    </div>
                    <div style={{ gridColumn: 'span 2' }}>
                      <label style={{ display: 'block', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>Customer Profile / Risk Flag</label>
                      <input 
                        type="text" 
                        value={builderProfile} 
                        onChange={(e) => setBuilderProfile(e.target.value)}
                        style={{ width: '100%', padding: '0.4rem 0.6rem', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '0.825rem' }} 
                      />
                    </div>
                  </div>


                  <button
                    onClick={handleBuildScenario}
                    style={{
                      width: '100%',
                      padding: '0.55rem',
                      borderRadius: '8px',
                      background: 'var(--accent-indigo)',
                      color: '#ffffff',
                      border: 'none',
                      fontWeight: 700,
                      fontSize: '0.85rem',
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      gap: '0.4rem',
                    }}
                  >
                    <Send size={14} />
                    <span>Generate Scenario & Run Dual-Agent Deliberation</span>
                  </button>
                </div>
              )}
            </div>

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
