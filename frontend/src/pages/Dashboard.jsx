import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import api from '../services/api';
import { ShieldAlert, TrendingUp, Wallet, TrendingDown, Target, BrainCircuit, AlertTriangle, Plus } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const RiskGauge = ({ score, label }) => {
  const rotation = Math.max(0, Math.min(180, (score / 100) * 180));
  const color = label === 'High Risk' ? 'var(--accent-warning)' : label === 'Medium Risk' ? 'var(--text-secondary)' : 'var(--accent-profit)';
  
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', margin: '2rem 0' }}>
      <div style={{ position: 'relative', width: '200px', height: '100px', overflow: 'hidden' }}>
        <div style={{ position: 'absolute', top: '0', left: '0', width: '200px', height: '200px', borderRadius: '50%', border: '20px solid var(--bg-base)', borderBottomColor: 'transparent', borderRightColor: 'transparent', transform: 'rotate(45deg)' }} />
        <div style={{ position: 'absolute', top: '0', left: '0', width: '200px', height: '200px', borderRadius: '50%', border: `20px solid ${color}`, borderBottomColor: 'transparent', borderRightColor: 'transparent', transform: `rotate(${45 + rotation}deg)`, transition: 'transform 1s ease-out' }} />
      </div>
      <h2 style={{ color, marginTop: '1rem' }}>{score}% - {label}</h2>
      <p style={{ color: 'var(--text-secondary)' }}>Neural Network Score</p>
    </div>
  );
};

const Dashboard = () => {
  const { user } = useContext(AuthContext);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  const [profileLoading, setProfileLoading] = useState(false);
  const [profileData, setProfileData] = useState({
    monthly_income: 150000,
    monthly_expenses: 50000,
    total_savings: 200000,
    loan_amount: 0,
    monthly_emi: 0,
    credit_score: 750,
    credit_card_usage: 10
  });

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await api.get('/analysis/dashboard');
      setData(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleProfileSubmit = async (e) => {
    e.preventDefault();
    setProfileLoading(true);
    try {
      await api.post('/profile', {
        ...profileData,
        monthly_income: parseFloat(profileData.monthly_income),
        monthly_expenses: parseFloat(profileData.monthly_expenses),
        total_savings: parseFloat(profileData.total_savings),
        loan_amount: parseFloat(profileData.loan_amount),
        monthly_emi: parseFloat(profileData.monthly_emi),
        credit_score: parseInt(profileData.credit_score),
        credit_card_usage: parseFloat(profileData.credit_card_usage) / 100.0,
      });
      await fetchData();
    } catch (err) {
      console.error(err);
    } finally {
      setProfileLoading(false);
    }
  };

  if (loading) return <div style={{ textAlign: 'center', marginTop: '4rem' }}>Analyzing Financial Profile...</div>;
  if (!data) return (
    <div className="dashboard-grid">
      <div className="col-span-12 glass-panel" style={{ maxWidth: '600px', margin: '4rem auto 0 auto', width: '100%' }}>
        <h2 style={{ marginBottom: '1rem', textAlign: 'center' }}>Initialize AI Financial Profile</h2>
        <p className="subtitle" style={{ textAlign: 'center', marginBottom: '2rem' }}>Please provide your baseline metrics to unlock AI predictions.</p>
        <form onSubmit={handleProfileSubmit}>
          <div className="form-group"><label>Monthly Income (₹)</label><input type="number" className="form-input" value={profileData.monthly_income} onChange={e=>setProfileData({...profileData, monthly_income: e.target.value})} required/></div>
          <div className="form-group"><label>Monthly Expenses (₹)</label><input type="number" className="form-input" value={profileData.monthly_expenses} onChange={e=>setProfileData({...profileData, monthly_expenses: e.target.value})} required/></div>
          <div className="form-group"><label>Total Savings (₹)</label><input type="number" className="form-input" value={profileData.total_savings} onChange={e=>setProfileData({...profileData, total_savings: e.target.value})} required/></div>
          <div className="form-group"><label>Credit Score (300-900)</label><input type="number" className="form-input" value={profileData.credit_score} onChange={e=>setProfileData({...profileData, credit_score: e.target.value})} required/></div>
          <button type="submit" className="btn-primary" style={{ width: '100%', marginTop: '1rem' }} disabled={profileLoading}>{profileLoading ? 'Initializing Neural Engines...' : 'Save & Boot Engines'}</button>
        </form>
      </div>
    </div>
  );

  return (
    <div>
      <header style={{ marginBottom: '2rem' }}>
        <h1>Executive Overview</h1>
        <p className="subtitle">Welcome back, {user?.username}. Here is your AI-driven financial status.</p>
      </header>

      <div className="dashboard-grid">
        {/* Metric Cards */}
        <div className="col-span-4 glass-panel" style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <div style={{ padding: '1rem', backgroundColor: 'rgba(255,255,255,0.05)', borderRadius: '12px' }}><Wallet size={24} className="text-ai" /></div>
          <div><p className="subtitle">Disposable</p><h3>₹{data.investment_capacity.disposable_income}</h3></div>
        </div>
        <div className="col-span-4 glass-panel" style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <div style={{ padding: '1rem', backgroundColor: 'rgba(16, 185, 129, 0.1)', borderRadius: '12px' }}><TrendingUp size={24} className="text-profit" /></div>
          <div><p className="subtitle">Safe Investment</p><h3>₹{data.investment_capacity.safe_monthly_investment}</h3></div>
        </div>
        <div className="col-span-4 glass-panel" style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <div style={{ padding: '1rem', backgroundColor: 'rgba(255,255,255,0.05)', borderRadius: '12px' }}><Target size={24} /></div>
          <div><p className="subtitle">Risk Tolerance</p><h3>{data.investment_capacity.risk_tolerance}</h3></div>
        </div>

        {/* AI Risk Meter */}
        <div className="col-span-4 glass-panel" style={{ textAlign: 'center' }}>
          <h3><BrainCircuit style={{ display: 'inline', verticalAlign: 'middle', marginRight: '8px' }} size={20} className="text-ai" /> AI Risk Assessment</h3>
          <RiskGauge score={data.risk_assessment.risk_score} label={data.risk_assessment.risk_label} />
          <p className="subtitle" style={{ fontSize: '0.875rem' }}>Default Probability: {(data.risk_assessment.details.default_probability * 100).toFixed(1)}%</p>
        </div>

        {/* Spending Forecast */}
        <div className="col-span-8 glass-panel">
          <h3>Spending Forecast (Prophet AI)</h3>
          {data.transactions_count > 0 ? (
            <div style={{ height: '300px', width: '100%', marginTop: '2rem' }}>
              <ResponsiveContainer>
                <LineChart data={data.spending_forecast.predictions}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                  <XAxis dataKey="date" stroke="rgba(255,255,255,0.5)" tick={{ fontSize: 12 }} />
                  <YAxis stroke="rgba(255,255,255,0.5)" tick={{ fontSize: 12 }} />
                  <Tooltip contentStyle={{ backgroundColor: 'var(--bg-surface)', border: '1px solid var(--border-color)', borderRadius: '8px' }} />
                  <Line type="monotone" dataKey="predicted_spend" stroke="var(--accent-ai)" strokeWidth={3} dot={false} activeDot={{ r: 8 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <div style={{ height: '200px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-secondary)' }}>
              Cannot forecast without transaction history. Estimated profile monthly burn: ₹{data.spending_forecast.estimated_monthly_spend}
            </div>
          )}
        </div>

        {/* Recommendations & Anomalies */}
        <div className="col-span-6 glass-panel">
          <h3>Budget Optimization</h3>
          <ul style={{ paddingLeft: '1.5rem', marginTop: '1rem', color: 'var(--text-secondary)' }}>
            {data.budget_optimization.recommendations.map((rec, i) => <li key={i} style={{ marginBottom: '0.5rem' }}>{rec}</li>)}
          </ul>
        </div>

        <div className="col-span-6 glass-panel" style={{ border: data.recent_anomalies?.length > 0 ? '1px solid rgba(239, 68, 68, 0.3)' : '1px solid var(--border-color)' }}>
          <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: data.recent_anomalies?.length > 0 ? 'var(--accent-warning)' : 'var(--text-primary)' }}>
            <ShieldAlert size={20} /> Isolation Forest Anomalies
          </h3>
          <div style={{ marginTop: '1rem', color: 'var(--text-secondary)' }}>
            {data.transactions_count === 0 ? "No live ledger data strictly available to scan." : 
              (data.recent_anomalies?.length === 0 ? "Analyzing live stream... No critical flag points detected currently." : 
                (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                    {data.recent_anomalies.slice(0, 4).map((anomaly, idx) => (
                       <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0.75rem', backgroundColor: 'rgba(239, 68, 68, 0.1)', borderRadius: '8px', borderLeft: '3px solid var(--accent-warning)' }}>
                          <div>
                            <div style={{ fontWeight: 600, color: 'var(--text-primary)'}}>{anomaly.description}</div>
                            <div style={{ fontSize: '0.75rem' }}>{anomaly.date} • {anomaly.severity} Severity</div>
                          </div>
                          <div style={{ fontWeight: 600, color: 'var(--accent-warning)' }}>₹{anomaly.amount.toLocaleString()}</div>
                       </div>
                    ))}
                  </div>
                )
              )
            }
          </div>
        </div>

      </div>
    </div>
  );
};

export default Dashboard;
