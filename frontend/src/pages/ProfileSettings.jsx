import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { UserCog } from 'lucide-react';

const ProfileSettings = () => {
  const [profile, setProfile] = useState({
    monthly_income: '',
    monthly_expenses: '',
    total_savings: '',
    loan_amount: '',
    monthly_emi: '',
    credit_score: '',
    credit_card_usage: ''
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await api.get('/profile');
        if (res.data) {
          setProfile({
            monthly_income: res.data.monthly_income || '',
            monthly_expenses: res.data.monthly_expenses || '',
            total_savings: res.data.total_savings || '',
            loan_amount: res.data.loan_amount || '0',
            monthly_emi: res.data.monthly_emi || '0',
            credit_score: res.data.credit_score || '',
            credit_card_usage: res.data.credit_card_usage !== undefined ? res.data.credit_card_usage : '0'
          });
        }
      } catch (err) {
        console.error("Failed to fetch profile", err);
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage({ type: '', text: '' });
    try {
      await api.post('/profile', {
        monthly_income: parseFloat(profile.monthly_income),
        monthly_expenses: parseFloat(profile.monthly_expenses),
        total_savings: parseFloat(profile.total_savings),
        loan_amount: parseFloat(profile.loan_amount) || 0,
        monthly_emi: parseFloat(profile.monthly_emi) || 0,
        credit_score: parseInt(profile.credit_score),
        credit_card_usage: parseFloat(profile.credit_card_usage) || 0
      });
      setMessage({ type: 'success', text: 'Financial profile universally updated successfully!' });
    } catch (err) {
      setMessage({ type: 'error', text: 'Error saving profile parameters.' });
    } finally {
      setSaving(false);
    }
  };

  const handleChange = (e) => {
    setProfile(prev => ({...prev, [e.target.name]: e.target.value}));
  };

  if (loading) return <div style={{ textAlign: 'center', marginTop: '4rem' }}>Loading Configuration Core...</div>;

  return (
    <div>
      <header style={{ marginBottom: '2rem' }}>
        <h1>Global Settings Matrix</h1>
        <p className="subtitle">Tune your raw financial predictive components. Data synced flawlessly to Dashboard AI.</p>
      </header>

      <div className="glass-panel" style={{ maxWidth: '700px', padding: '2.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem' }}>
          <UserCog size={32} className="text-ai" />
          <h2 style={{ margin: 0 }}>Predictive Profile Configuration</h2>
        </div>

        {message.text && (
          <div style={{ backgroundColor: message.type === 'success' ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)', color: message.type === 'success' ? 'var(--accent-profit)' : 'var(--accent-warning)', padding: '0.75rem', borderRadius: '8px', marginBottom: '1.5rem', fontSize: '0.875rem', border: `1px solid ${message.type === 'success' ? 'rgba(16, 185, 129, 0.2)' : 'rgba(239, 68, 68, 0.2)'}` }}>
            {message.text}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '1.5rem' }}>
            <div className="form-group" style={{ marginBottom: 0 }}>
              <label>Monthly Income</label>
              <input type="number" name="monthly_income" className="form-input" value={profile.monthly_income} onChange={handleChange} required min="0" />
            </div>
            <div className="form-group" style={{ marginBottom: 0 }}>
              <label>Monthly Expenses</label>
              <input type="number" name="monthly_expenses" className="form-input" value={profile.monthly_expenses} onChange={handleChange} required min="0" />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '1.5rem' }}>
            <div className="form-group" style={{ marginBottom: 0 }}>
              <label>Total Savings</label>
              <input type="number" name="total_savings" className="form-input" value={profile.total_savings} onChange={handleChange} required min="0" />
            </div>
            <div className="form-group" style={{ marginBottom: 0 }}>
              <label>Credit Score</label>
              <input type="number" name="credit_score" className="form-input" value={profile.credit_score} onChange={handleChange} required min="300" max="850" />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '2rem' }}>
            <div className="form-group" style={{ marginBottom: 0 }}>
              <label>Loan Amount</label>
              <input type="number" name="loan_amount" className="form-input" value={profile.loan_amount} onChange={handleChange} min="0" />
            </div>
            <div className="form-group" style={{ marginBottom: 0 }}>
              <label>Monthly EMI</label>
              <input type="number" name="monthly_emi" className="form-input" value={profile.monthly_emi} onChange={handleChange} min="0" />
            </div>
          </div>
          
          <div className="form-group" style={{ marginBottom: '2.5rem' }}>
            <label>Credit Card Usage %</label>
            <input type="number" name="credit_card_usage" className="form-input" value={profile.credit_card_usage} onChange={handleChange} min="0" max="100" />
          </div>

          <button type="submit" className="btn-primary" style={{ width: '100%', padding: '0.875rem' }} disabled={saving}>
            {saving ? 'Syncing to Neural Core...' : 'Sync Settings'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default ProfileSettings;
