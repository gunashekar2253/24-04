import React, { useContext } from 'react';
import { NavLink } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { BrainCircuit, LineChart, MessageSquare, Target, LogOut, Wallet } from 'lucide-react';

const Navbar = () => {
  const { logout, user } = useContext(AuthContext);

  return (
    <nav className="navbar">
      <div className="nav-brand">
        <BrainCircuit size={28} className="text-ai" />
        <span>Finance</span> AI
      </div>

      <div className="nav-links">
        <NavLink to="/dashboard" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <LineChart size={18} /> Dashboard
        </NavLink>
        <NavLink to="/add-details" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Wallet size={18} /> Ledger
        </NavLink>
        <NavLink to="/assistant" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <MessageSquare size={18} /> AI Assistant
        </NavLink>
        <NavLink to="/stocks" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <LineChart size={18} /> Stocks
        </NavLink>
        <NavLink to="/goals" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Target size={18} /> Goals
        </NavLink>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
        <span style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
          {user?.username}
        </span>
        <button onClick={logout} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-secondary)', transition: 'color 0.2s' }} onMouseOver={(e) => e.target.style.color = 'var(--text-primary)'} onMouseOut={(e) => e.target.style.color = 'var(--text-secondary)'}>
          <LogOut size={18} /> Logout
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
