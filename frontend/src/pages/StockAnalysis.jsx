import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Search, BrainCircuit, LineChart, MessageSquare, Briefcase } from 'lucide-react';
import { ResponsiveContainer, LineChart as RechartsLineChart, Line, XAxis, YAxis, Tooltip } from 'recharts';
import ReactMarkdown from 'react-markdown';

import { useLocation } from 'react-router-dom';

const StockAnalysis = () => {
  const location = useLocation();
  const [tickerSearch, setTickerSearch] = useState('');
  const [stockData, setStockData] = useState(null);
  const [aiAnalysis, setAiAnalysis] = useState('');
  const [loadingSearch, setLoadingSearch] = useState(false);
  
  const [chatMessages, setChatMessages] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [chatLoading, setChatLoading] = useState(false);

  const fetchStockData = async (tickerValue) => {
    if (!tickerValue) return;
    setLoadingSearch(true);
    setStockData(null);
    setAiAnalysis('');
    setChatMessages([]);

    try {
      const res = await api.get(`/stocks/analyze/${tickerValue}`);
      setStockData(res.data.stock_data);
      setAiAnalysis(res.data.ai_analysis);
      
      // Seed first chat message
      setChatMessages([{
        sender: 'ai',
        text: `I am the CrewAI specialist assigned to ${res.data.stock_data.ticker}. Reading current fundamentals... How can I assist?`
      }]);
    } catch (err) {
      console.error(err);
      alert("Error fetching stock data. Check API connection or validity of ticker.");
    } finally {
      setLoadingSearch(false);
    }
  };

  const handleSearch = async (e) => {
    e?.preventDefault();
    fetchStockData(tickerSearch);
  };

  useEffect(() => {
    if (location.state?.searchTicker) {
       setTickerSearch(location.state.searchTicker);
       fetchStockData(location.state.searchTicker);
       window.history.replaceState({}, document.title);
    }
  }, [location.state]);

  const handleChat = async (e) => {
    e.preventDefault();
    if (!chatInput.trim() || !stockData) return;

    const userMessage = { sender: 'user', text: chatInput };
    setChatMessages(prev => [...prev, userMessage]);
    setChatInput('');
    setChatLoading(true);

    try {
      const res = await api.post('/stocks/chat', { ticker: stockData.ticker, question: userMessage.text });
      setChatMessages(prev => [...prev, { sender: 'ai', text: res.data.answer }]);
    } catch (err) {
      setChatMessages(prev => [...prev, { sender: 'ai', text: "Error fetching data from CrewAI cluster." }]);
    } finally {
      setChatLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <header style={{ marginBottom: '2rem' }}>
        <h1>Equities Engine</h1>
        <p className="subtitle">Real-time yFinance streaming integrated with CrewAI analysis.</p>
        
        <form onSubmit={handleSearch} style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem', maxWidth: '500px' }}>
          <div style={{ position: 'relative', flex: 1 }}>
            <Search size={18} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-secondary)' }} />
            <input 
              type="text" 
              className="form-input" 
              style={{ width: '100%', paddingLeft: '2.5rem' }} 
              placeholder="Search ticker (e.g. AAPL, RELIANCE.NS)"
              value={tickerSearch}
              onChange={(e) => setTickerSearch(e.target.value.toUpperCase())}
            />
          </div>
          <button type="submit" className="btn-primary" disabled={loadingSearch}>
            {loadingSearch ? 'Analyzing...' : 'Execute'}
          </button>
        </form>
      </header>

      {stockData && (
        <div style={{ display: 'flex', gap: '1.5rem', height: 'calc(100vh - 250px)' }}>
          {/* Left Pane: Stock Data */}
          <div className="glass-panel" style={{ flex: 6, display: 'flex', flexDirection: 'column', overflowY: 'auto' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '2rem' }}>
              <div>
                <h1 style={{ margin: 0 }}>{stockData.ticker}</h1>
                <h3 className="subtitle" style={{ margin: 0 }}>{stockData.name}</h3>
                <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem', marginTop: '0.5rem', background: 'rgba(255,255,255,0.05)', padding: '0.25rem 0.75rem', borderRadius: '4px', fontSize: '0.875rem' }}>
                  <Briefcase size={14} /> {stockData.sector} • {stockData.industry}
                </div>
              </div>
              <div style={{ textAlign: 'right' }}>
                <h1 style={{ margin: 0 }}>₹{stockData.current_price?.toLocaleString() || stockData.current_price}</h1>
                <p style={{ color: 'var(--text-secondary)' }}>Market Cap: ₹{stockData.market_cap?.toLocaleString()}</p>
              </div>
            </div>

            <div style={{ height: '250px', marginBottom: '2rem' }}>
              <ResponsiveContainer>
                <RechartsLineChart data={stockData.price_history}>
                  <XAxis dataKey="date" hide />
                  <YAxis domain={['auto', 'auto']} hide />
                  <Tooltip contentStyle={{ backgroundColor: 'var(--bg-surface)', border: 'none', borderRadius: '8px' }} />
                  <Line type="monotone" dataKey="close" stroke="var(--accent-ai)" strokeWidth={2} dot={false} />
                </RechartsLineChart>
              </ResponsiveContainer>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1rem', marginBottom: '2rem' }}>
              <div style={{ backgroundColor: 'rgba(255,255,255,0.02)', padding: '1rem', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
                <p className="subtitle" style={{ fontSize: '0.875rem', marginBottom: '0.25rem' }}>P/E Ratio</p>
                <h3 style={{ margin: 0 }}>{stockData.pe_ratio || 'N/A'}</h3>
              </div>
              <div style={{ backgroundColor: 'rgba(255,255,255,0.02)', padding: '1rem', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
                <p className="subtitle" style={{ fontSize: '0.875rem', marginBottom: '0.25rem' }}>52W Range</p>
                <h3 style={{ margin: 0, fontSize: '1.1rem' }}>{stockData['52_week_low']} - {stockData['52_week_high']}</h3>
              </div>
            </div>

            <div>
              <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}><LineChart size={18} className="text-ai" /> CrewAI Fundamental Analysis</h3>
              <div style={{ backgroundColor: 'rgba(139, 92, 246, 0.05)', border: '1px solid rgba(139, 92, 246, 0.2)', padding: '1.5rem', borderRadius: '8px', lineHeight: '1.6' }}>
                <ReactMarkdown>{aiAnalysis}</ReactMarkdown>
              </div>
            </div>
          </div>

          {/* Right Pane: Stock Agent Chat */}
          <div className="glass-panel" style={{ flex: 4, display: 'flex', flexDirection: 'column', padding: 0, overflow: 'hidden' }}>
            <div style={{ padding: '1rem 1.5rem', borderBottom: '1px solid var(--border-color)', backgroundColor: 'rgba(255,255,255,0.02)', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <MessageSquare size={18} className="text-ai" />
              <h3 style={{ margin: 0, fontSize: '1rem' }}>Direct Line: Analyst Agent</h3>
            </div>
            
            <div style={{ flex: 1, overflowY: 'auto', padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {chatMessages.map((msg, i) => (
                <div key={i} style={{ alignSelf: msg.sender === 'user' ? 'flex-end' : 'flex-start', maxWidth: '85%' }}>
                   <div style={{ 
                    background: msg.sender === 'user' ? 'rgba(255,255,255,0.05)' : 'rgba(139,92,246,0.1)',
                    border: `1px solid ${msg.sender === 'user' ? 'var(--border-color)' : 'rgba(139,92,246,0.3)'}`,
                    padding: '0.75rem 1rem',
                    borderRadius: '12px',
                    borderTopRightRadius: msg.sender === 'user' ? '2px' : '12px',
                    borderTopLeftRadius: msg.sender === 'ai' ? '2px' : '12px',
                    color: 'var(--text-primary)',
                    fontSize: '0.875rem',
                    lineHeight: '1.5'
                  }}>
                    <ReactMarkdown>{msg.text}</ReactMarkdown>
                  </div>
                </div>
              ))}
              {chatLoading && <div style={{ color: 'var(--accent-ai)', fontSize: '0.875rem' }}>Agent is typing...</div>}
            </div>

            <div style={{ padding: '1rem', borderTop: '1px solid var(--border-color)', backgroundColor: 'var(--bg-base)' }}>
              <form onSubmit={handleChat} style={{ display: 'flex' }}>
                <input 
                  type="text" 
                  className="form-input" 
                  style={{ flex: 1, borderRadius: '4px 0 0 4px', borderRight: 'none', backgroundColor: 'transparent' }} 
                  placeholder={`Ask about ${stockData.ticker}...`}
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  disabled={chatLoading}
                />
                <button type="submit" className="btn-primary" style={{ borderRadius: '0 4px 4px 0', padding: '0 1rem' }} disabled={chatLoading}>
                  Send
                </button>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default StockAnalysis;
