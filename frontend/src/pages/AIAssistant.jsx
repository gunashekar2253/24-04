import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import { Send, BrainCircuit, ShieldCheck, User as UserIcon } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

const AIAssistant = () => {
  const navigate = useNavigate();
  const [messages, setMessages] = useState(() => {
    const saved = localStorage.getItem('aiAssistantChat');
    if (saved) {
      return JSON.parse(saved);
    }
    return [{
      id: 1,
      sender: 'ai',
      text: "Hello. I am your specialized Finance AI Assistant powered by Google Gemini. How can I assist with your financial strategizing today?",
      is_finance: true
    }];
  });
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    localStorage.setItem('aiAssistantChat', JSON.stringify(messages));
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { id: Date.now(), sender: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const res = await api.post('/query/', { query: userMessage.text });

      if (res.data.response.startsWith("REDIRECT_TO_STOCK:")) {
        const ticker = res.data.response.replace("REDIRECT_TO_STOCK:", "").trim();

        setMessages(prev => [...prev, {
          id: Date.now() + 1,
          sender: 'ai',
          text: `Routing link successful. Redirecting terminal to Equities Engine for ${ticker}...`,
          is_finance: true
        }]);

        setTimeout(() => navigate('/stocks', { state: { searchTicker: ticker } }), 800);
        return;
      }

      const aiMessage = {
        id: Date.now() + 1,
        sender: 'ai',
        text: res.data.response,
        is_finance: res.data.is_finance,
        reason: res.data.classification_reason
      };
      setMessages(prev => [...prev, aiMessage]);
    } catch (err) {
      setMessages(prev => [...prev, { id: Date.now() + 1, sender: 'ai', text: "Error connecting to AI compute core.", is_finance: false }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: 'calc(100vh - 100px)' }}>
      <header style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <h1>Strategic Advisor</h1>
          {/* <p className="subtitle">Direct neural link to your financial advisory unit.</p> */}
        </div>
        <div className="ai-indicator">
          <div className="ai-indicator-dot" /> 🔒 Finance Specialization Active
        </div>
      </header>

      <div className="glass-panel" style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden', padding: 0 }}>
        {/* Chat Feed */}
        <div style={{ flex: 1, overflowY: 'auto', padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {messages.map(msg => (
            <div key={msg.id} style={{ display: 'flex', gap: '1rem', alignSelf: msg.sender === 'user' ? 'flex-end' : 'flex-start', maxWidth: '80%' }}>
              {msg.sender === 'ai' && (
                <div style={{ width: '40px', height: '40px', borderRadius: '50%', background: 'linear-gradient(135deg, var(--accent-ai), #C084FC)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0, boxShadow: '0 0 15px rgba(139,92,246,0.3)' }}>
                  <BrainCircuit size={20} color="white" />
                </div>
              )}

              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                <div style={{
                  background: msg.sender === 'user' ? 'rgba(255,255,255,0.05)' : (!msg.is_finance ? 'rgba(239, 68, 68, 0.1)' : 'rgba(139,92,246,0.1)'),
                  border: `1px solid ${msg.sender === 'user' ? 'var(--border-color)' : (!msg.is_finance ? 'rgba(239, 68, 68, 0.3)' : 'rgba(139,92,246,0.3)')}`,
                  padding: '1rem 1.5rem',
                  borderRadius: '16px',
                  borderTopRightRadius: msg.sender === 'user' ? '4px' : '16px',
                  borderTopLeftRadius: msg.sender === 'ai' ? '4px' : '16px',
                  color: 'var(--text-primary)',
                  lineHeight: '1.6'
                }}>
                  <ReactMarkdown>{msg.text}</ReactMarkdown>
                </div>

                {msg.sender === 'ai' && msg.reason && !msg.is_finance && (
                  <div style={{ fontSize: '0.75rem', color: 'var(--accent-warning)', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                    <ShieldCheck size={12} /> {msg.reason}
                  </div>
                )}
              </div>

              {msg.sender === 'user' && (
                <div style={{ width: '40px', height: '40px', borderRadius: '50%', backgroundColor: 'var(--bg-surface)', border: '1px solid var(--border-color)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                  <UserIcon size={20} color="var(--text-secondary)" />
                </div>
              )}
            </div>
          ))}
          {loading && (
            <div style={{ alignSelf: 'flex-start', display: 'flex', gap: '1rem', alignItems: 'center' }}>
              <div style={{ width: '40px', height: '40px', borderRadius: '50%', background: 'linear-gradient(135deg, var(--accent-ai), #C084FC)', display: 'flex', alignItems: 'center', justifyContent: 'center', opacity: 0.5 }}>
                <BrainCircuit size={20} color="white" />
              </div>
              <div style={{ color: 'var(--accent-ai)' }}>Computing response...</div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Boundary */}
        <div style={{ borderTop: '1px solid var(--border-color)', padding: '1.5rem', backgroundColor: 'var(--bg-base)' }}>
          <form onSubmit={handleSend} style={{ display: 'flex', gap: '1rem' }}>
            <input
              type="text"
              className="form-input"
              style={{ flex: 1, backgroundColor: 'rgba(255,255,255,0.02)' }}
              placeholder="Ask for advice, budget plans, loan structures..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={loading}
            />
            <button type="submit" className="btn-primary" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0 2rem' }} disabled={loading}>
              <Send size={18} /> Transmit
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default AIAssistant;
