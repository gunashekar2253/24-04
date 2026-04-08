import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Target, CheckCircle2, Clock } from 'lucide-react';

const Goals = () => {
  const [goals, setGoals] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Form State
  const [name, setName] = useState('');
  const [targetAmount, setTargetAmount] = useState('');
  const [targetDate, setTargetDate] = useState('');
  const [currentAmount, setCurrentAmount] = useState('');

  // AI Plan State
  const [aiPlan, setAiPlan] = useState(null);
  const [computingPlanFor, setComputingPlanFor] = useState(null);

  const fetchGoals = async () => {
    try {
      const res = await api.get('/goals');
      setGoals(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGoals();
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await api.post('/goals', {
        name,
        target_amount: parseFloat(targetAmount),
        target_date: targetDate,
        current_amount: currentAmount ? parseFloat(currentAmount) : 0
      });
      setName(''); setTargetAmount(''); setTargetDate(''); setCurrentAmount('');
      fetchGoals();
    } catch (err) {
      console.error(err);
    }
  };

  const generateAIPlan = async (goalId) => {
    setComputingPlanFor(goalId);
    try {
      const res = await api.post(`/goals/${goalId}/plan`);
      setAiPlan(res.data);
    } catch (err) {
      alert("Failed to compute AI Plan.");
    } finally {
      setComputingPlanFor(null);
    }
  };

  if (loading) return null;

  return (
    <div className="dashboard-grid">
      <div className="col-span-12">
        <h1>Capital Objectives</h1>
        <p className="subtitle">Set targets. Let the Engine calculate the exact velocity required.</p>
      </div>

      {/* Goal Creation Form */}
      <div className="col-span-5 glass-panel">
        <h3>New Objective</h3>
        <form onSubmit={handleCreate} style={{ marginTop: '1.5rem' }}>
          <div className="form-group">
            <label>Objective Name</label>
            <input type="text" className="form-input" value={name} onChange={e => setName(e.target.value)} required placeholder="e.g. House Downpayment" />
          </div>
          <div style={{ display: 'flex', gap: '1rem' }}>
            <div className="form-group" style={{ flex: 1 }}>
              <label>Target Amount (₹)</label>
              <input type="number" className="form-input" value={targetAmount} onChange={e => setTargetAmount(e.target.value)} required />
            </div>
            <div className="form-group" style={{ flex: 1 }}>
              <label>Current Saved (₹)</label>
              <input type="number" className="form-input" value={currentAmount} onChange={e => setCurrentAmount(e.target.value)} />
            </div>
          </div>
          <div className="form-group" style={{ marginBottom: '2rem' }}>
            <label>Target Horizon Date</label>
            <input type="date" className="form-input" value={targetDate} onChange={e => setTargetDate(e.target.value)} required />
          </div>
          <button type="submit" className="btn-primary" style={{ width: '100%' }}>Initiate Directive</button>
        </form>
      </div>

      {/* Goals Display List */}
      <div className="col-span-7" style={{ display: 'flex', gap: '1.5rem', flexDirection: 'column' }}>
        {goals.map(goal => {
          const progress = Math.min(100, (goal.current_amount / goal.target_amount) * 100).toFixed(1);
          const isComplete = progress >= 100;

          return (
            <div key={goal.id} className="glass-panel" style={{ display: 'flex', flexDirection: 'column', gap: '1rem', border: isComplete ? '1px solid var(--accent-profit)' : '1px solid var(--border-color)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <h3 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    {isComplete ? <CheckCircle2 className="text-profit" /> : <Target className="text-ai" />}
                    {goal.name}
                  </h3>
                  <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginTop: '0.25rem' }}>Deadline: {new Date(goal.target_date).toLocaleDateString()}</div>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <h3 style={{ margin: 0 }}>₹{goal.current_amount.toLocaleString()} <span style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', fontWeight: 500 }}>/ ₹{goal.target_amount.toLocaleString()}</span></h3>
                  <div style={{ color: 'var(--accent-ai)', fontWeight: 600 }}>{progress}% Validated</div>
                </div>
              </div>

              {/* Progress Bar Track */}
              <div style={{ width: '100%', height: '8px', backgroundColor: 'rgba(255,255,255,0.05)', borderRadius: '4px', overflow: 'hidden' }}>
                <div style={{ width: `${progress}%`, height: '100%', backgroundColor: isComplete ? 'var(--accent-profit)' : 'var(--accent-ai)', transition: 'width 1s ease-in-out' }} />
              </div>

              {!isComplete && (
                <div style={{ alignSelf: 'flex-end', marginTop: '0.5rem' }}>
                  <button onClick={() => generateAIPlan(goal.id)} className="btn-secondary" style={{ fontSize: '0.875rem', padding: '0.5rem 1rem' }} disabled={computingPlanFor === goal.id}>
                    {computingPlanFor === goal.id ? 'Computing Engine Path...' : 'Engage AI Timeline Computation'}
                  </button>
                </div>
              )}
            </div>
          );
        })}

        {goals.length === 0 && (
          <div className="glass-panel" style={{ textAlign: 'center', padding: '4rem 0', color: 'var(--text-secondary)' }}>
            No capital objectives locked in. Set a perimeter.
          </div>
        )}
      </div>

      {/* Conditional Rendering logic for AI Output Panel */}
      {aiPlan && (
        <div className="col-span-12 glass-panel" style={{ border: '1px solid var(--accent-ai)', marginTop: '1rem', background: 'rgba(139, 92, 246, 0.03)' }}>
          <h2 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--accent-ai)' }}>
            <BrainCircuit size={24} /> Engine Path: {aiPlan.goal_name}
          </h2>
          
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem', marginTop: '2rem' }}>
             <div>
               <p className="subtitle">Feasibility Engine Check</p>
               <h3 style={{ color: aiPlan.feasible ? 'var(--accent-profit)' : 'var(--accent-warning)' }}>
                 {aiPlan.feasible ? 'GO (Cleared)' : 'NO-GO (Red Line)'}
               </h3>
             </div>
             <div>
               <p className="subtitle">Monthly Delta Requirement</p>
               <h3>₹{aiPlan.monthly_contribution.toLocaleString()} / mo</h3>
             </div>
             <div>
               <p className="subtitle">Velocity Timeline</p>
               <h3>{aiPlan.timeline || 'Infinite'}</h3>
             </div>
          </div>

          {!aiPlan.feasible && (
             <div style={{ marginTop: '1.5rem', color: 'var(--accent-warning)', padding: '1rem', backgroundColor: 'rgba(239, 68, 68, 0.1)', borderRadius: '8px' }}>
                CRITICAL WARNING: {aiPlan.message}
             </div>
          )}
          
          {aiPlan.feasible && (
            <div style={{ marginTop: '2.5rem' }}>
              <h4 style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}><Clock size={16} style={{ display: 'inline', verticalAlign: 'text-bottom' }} /> Milestone Checkpoints</h4>
              <div style={{ display: 'flex', justifyContent: 'space-between', borderTop: '1px dashed var(--border-color)', position: 'relative' }}>
                <div style={{ position: 'absolute', top: -5, width: '100%', height: '10px', display: 'flex', justifyContent: 'space-between' }}>
                  {aiPlan.milestones.map((m, i) => <div key={i} style={{ width: '10px', height: '10px', borderRadius: '50%', background: 'var(--bg-surface)', border: '2px solid var(--accent-ai)' }} />)}
                </div>
                {aiPlan.milestones.map((m, i) => (
                  <div key={i} style={{ paddingTop: '1.5rem', textAlign: 'center', width: '25%' }}>
                    <div style={{ fontWeight: 600 }}>{m.percentage}% Sub-sector</div>
                    <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>In {m.months} months</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Goals;
