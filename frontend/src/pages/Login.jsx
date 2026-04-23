import React, { useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { BrainCircuit } from 'lucide-react';

const Login = () => {
  const { login, register } = useContext(AuthContext);
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [age, setAge] = useState('');
  const [monthlyIncome, setMonthlyIncome] = useState('');
  const [monthlyExpenses, setMonthlyExpenses] = useState('');
  const [totalSavings, setTotalSavings] = useState('');
  const [loanAmount, setLoanAmount] = useState('');
  const [monthlyEmi, setMonthlyEmi] = useState('');
  const [creditScore, setCreditScore] = useState('');
  const [creditCardUsage, setCreditCardUsage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    if (isLogin) {
      const res = await login(username, password);
      if (!res.success) setError(res.message);
    } else {
      const res = await register({ 
        username, 
        password, 
        age: parseInt(age), 
        currency: 'INR',
        monthly_income: parseFloat(monthlyIncome),
        monthly_expenses: parseFloat(monthlyExpenses),
        total_savings: parseFloat(totalSavings),
        loan_amount: parseFloat(loanAmount) || 0,
        monthly_emi: parseFloat(monthlyEmi) || 0,
        credit_score: parseInt(creditScore),
        credit_card_usage: parseFloat(creditCardUsage) || 0
      });
      if (!res.success) setError(res.message);
    }

    setLoading(false);
  };

  return (
    <div style={{ display: 'flex', minHeight: '100vh', alignItems: 'center', justifyContent: 'center', backgroundColor: 'var(--bg-base)' }}>
      <div className="glass-panel" style={{ width: '100%', maxWidth: isLogin ? '400px' : '650px', padding: '2.5rem', transition: 'max-width 0.3s ease' }}>
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <BrainCircuit size={48} className="text-ai" style={{ margin: '0 auto 1rem' }} />
          <h2 style={{ marginBottom: '0.5rem' }}>{isLogin ? 'Welcome Back' : 'Create Account'}</h2>
          <p className="subtitle">Enter your credentials to access Finance AI.</p>
        </div>

        {error && <div style={{ backgroundColor: 'rgba(239, 68, 68, 0.1)', color: 'var(--accent-warning)', padding: '0.75rem', borderRadius: '8px', marginBottom: '1.5rem', fontSize: '0.875rem', border: '1px solid rgba(239, 68, 68, 0.2)' }}>{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Username</label>
            <input type="text" className="form-input" value={username} onChange={(e) => setUsername(e.target.value)} required placeholder="Enter username" />
          </div>

          {!isLogin && (
            <>
              <div className="form-group" style={{ marginBottom: '1rem' }}>
                <label>Age</label>
                <input type="number" className="form-input" value={age} onChange={(e) => setAge(e.target.value)} required placeholder="Enter age" min="18" max="100" />
              </div>
              
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label>Monthly Income</label>
                  <input type="number" className="form-input" value={monthlyIncome} onChange={(e) => setMonthlyIncome(e.target.value)} required placeholder="e.g. 5000" min="0" />
                </div>
                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label>Monthly Expenses</label>
                  <input type="number" className="form-input" value={monthlyExpenses} onChange={(e) => setMonthlyExpenses(e.target.value)} required placeholder="e.g. 2000" min="0" />
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label>Total Savings</label>
                  <input type="number" className="form-input" value={totalSavings} onChange={(e) => setTotalSavings(e.target.value)} required placeholder="e.g. 10000" min="0" />
                </div>
                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label>Credit Score</label>
                  <input type="number" className="form-input" value={creditScore} onChange={(e) => setCreditScore(e.target.value)} required placeholder="300-850" min="300" max="850" />
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label>Loan Amt</label>
                  <input type="number" className="form-input" value={loanAmount} onChange={(e) => setLoanAmount(e.target.value)} placeholder="e.g. 0" min="0" />
                </div>
                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label>Monthly EMI</label>
                  <input type="number" className="form-input" value={monthlyEmi} onChange={(e) => setMonthlyEmi(e.target.value)} placeholder="e.g. 0" min="0" />
                </div>
                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label>CC Usage %</label>
                  <input type="number" className="form-input" value={creditCardUsage} onChange={(e) => setCreditCardUsage(e.target.value)} placeholder="0-100" min="0" max="100" />
                </div>
              </div>
            </>
          )}

          <div className="form-group" style={{ marginBottom: '2rem' }}>
            <label>Password</label>
            <input type="password" className="form-input" value={password} onChange={(e) => setPassword(e.target.value)} required placeholder="Enter password" minLength="6" />
          </div>

          <button type="submit" className="btn-primary" style={{ width: '100%', padding: '0.875rem' }} disabled={loading}>
            {loading ? 'Authenticating...' : (isLogin ? 'Sign In' : 'Sign Up')}
          </button>
        </form>

        <div style={{ textAlign: 'center', marginTop: '1.5rem', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
          {isLogin ? "Don't have an account? " : "Already have an account? "}
          <button type="button" onClick={() => setIsLogin(!isLogin)} style={{ color: 'var(--accent-ai)', fontWeight: '600' }}>
            {isLogin ? 'Sign Up' : 'Sign In'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Login;
