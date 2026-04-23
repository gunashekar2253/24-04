import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Plus, Trash2, ArrowUpRight, ArrowDownRight, Activity } from 'lucide-react';

const AddDetails = () => {
  const [transactions, setTransactions] = useState([]);
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const [description, setDescription] = useState('');
  const [amount, setAmount] = useState('');
  const [category, setCategory] = useState('Food');
  const [type, setType] = useState('expense');
  const [loading, setLoading] = useState(false);

  const fetchTransactions = async () => {
    try {
      const res = await api.get('/transactions');
      setTransactions(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchTransactions();
  }, []);

  useEffect(() => {
    if (type === 'income') {
      setCategory('Salary');
    } else {
      setCategory('Food & Dining');
    }
  }, [type]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.post('/transactions', {
        date,
        description,
        amount: parseFloat(amount),
        category,
        type
      });
      setDescription('');
      setAmount('');
      fetchTransactions();
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.delete(`/transactions/${id}`);
      fetchTransactions();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="dashboard-grid">
      <div className="col-span-12">
        <h1>Ledger Operations</h1>
        <p className="subtitle">Add your latest financial sweeps into the matrix.</p>
      </div>

      <div className="col-span-4 glass-panel">
        <h3>New Entry</h3>
        <form onSubmit={handleSubmit} style={{ marginTop: '1.5rem' }}>
          <div style={{ display: 'flex', gap: '1rem', marginBottom: '1.25rem' }}>
            <button type="button" onClick={() => setType('income')} className={type === 'income' ? 'btn-primary' : 'btn-secondary'} style={{ flex: 1, backgroundColor: type === 'income' ? 'var(--accent-profit)' : 'transparent', color: type==='income' ? 'white':'var(--text-primary)' }}>Income</button>
            <button type="button" onClick={() => setType('expense')} className={type === 'expense' ? 'btn-primary' : 'btn-secondary'} style={{ flex: 1, backgroundColor: type === 'expense' ? 'var(--accent-warning)' : 'transparent', color: type==='expense' ? 'white':'var(--text-primary)' }}>Expense</button>
          </div>

          <div className="form-group">
            <label>Date</label>
            <input type="date" className="form-input" value={date} onChange={(e) => setDate(e.target.value)} required />
          </div>
          <div className="form-group">
            <label>Amount (₹)</label>
            <input type="number" step="0.01" className="form-input" value={amount} onChange={(e) => setAmount(e.target.value)} required placeholder="0.00" />
          </div>
          <div className="form-group">
            <label>Category</label>
            <select className="form-input" value={category} onChange={(e) => setCategory(e.target.value)} required style={{ appearance: 'none' }}>
              {type === 'income' ? (
                <>
                  <option value="Salary">Salary</option>
                  <option value="Bonus">Bonus</option>
                  <option value="Freelance / Part-time">Freelance / Part-time</option>
                  <option value="Business Income">Business Income</option>
                  <option value="Investment Returns">Investment Returns</option>
                  <option value="Other Income">Other Income</option>
                </>
              ) : (
                <>
                  <option value="Food & Dining">Food & Dining</option>
                  <option value="Housing & Rent">Housing & Rent</option>
                  <option value="Transportation">Transportation</option>
                  <option value="Utilities">Utilities</option>
                  <option value="Entertainment">Entertainment</option>
                  <option value="Shopping">Shopping</option>
                  <option value="Healthcare">Healthcare</option>
                  <option value="Other Expenses">Other Expenses</option>
                </>
              )}
            </select>
          </div>
          <div className="form-group" style={{ marginBottom: '2rem' }}>
            <label>Description</label>
            <input type="text" className="form-input" value={description} onChange={(e) => setDescription(e.target.value)} required placeholder="Vendor name, notes..." />
          </div>
          <button type="submit" className="btn-primary" style={{ width: '100%', display: 'flex', justifyContent: 'center', gap: '0.5rem' }} disabled={loading}>
            <Plus size={20} /> {loading ? 'Logging...' : 'Execute Entry'}
          </button>
        </form>
      </div>

      <div className="col-span-8 glass-panel" style={{ height: '700px', overflowY: 'auto' }}>
        <h3>History Archive</h3>
        <div style={{ marginTop: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {transactions.map((tx) => (
            <div key={tx.id} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '1rem', backgroundColor: 'rgba(255,255,255,0.03)', borderRadius: '12px', border: '1px solid var(--border-color)', position: 'relative', overflow: 'hidden' }}>
              {/* Anomaly Indicator */}
              {tx.anomaly_analysis?.is_anomaly && (
                <div style={{ position: 'absolute', left: 0, top: 0, bottom: 0, width: '4px', backgroundColor: 'var(--accent-warning)', boxShadow: '0 0 10px var(--accent-warning)' }} />
              )}
              
              <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
                <div style={{ color: tx.type === 'income' ? 'var(--accent-profit)' : 'var(--text-secondary)' }}>
                  {tx.type === 'income' ? <ArrowUpRight size={24} /> : <ArrowDownRight size={24} />}
                </div>
                <div>
                  <h4 style={{ margin: 0 }}>{tx.description}</h4>
                  <div style={{ display: 'flex', gap: '1rem', color: 'var(--text-secondary)', fontSize: '0.875rem', marginTop: '0.25rem' }}>
                    <span>{new Date(tx.date).toLocaleDateString()}</span>
                    <span>•</span>
                    <span>{tx.category}</span>
                    {tx.anomaly_analysis?.is_anomaly && (
                      <span style={{ color: 'var(--accent-warning)', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                        <Activity size={14} /> Anomaly Tagged
                      </span>
                    )}
                  </div>
                </div>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '2rem' }}>
                <h3 style={{ margin: 0, color: tx.type === 'income' ? 'var(--accent-profit)' : 'var(--text-primary)' }}>
                  {tx.type === 'income' ? '+' : '-'}₹{tx.amount.toLocaleString()}
                </h3>
                <button onClick={() => handleDelete(tx.id)} style={{ color: 'var(--text-muted)' }} onMouseOver={(e) => e.target.style.color = 'var(--accent-warning)'} onMouseOut={(e) => e.target.style.color = 'var(--text-muted)'}>
                  <Trash2 size={18} />
                </button>
              </div>
            </div>
          ))}
          {transactions.length === 0 && <div style={{ textAlign: 'center', color: 'var(--text-secondary)', padding: '2rem' }}>Local ledger is empty.</div>}
        </div>
      </div>
    </div>
  );
};

export default AddDetails;
