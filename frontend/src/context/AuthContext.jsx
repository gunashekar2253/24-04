import React, { createContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';
import api from '../services/api';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('finance_ai_token');
      if (token) {
        try {
          const decoded = jwtDecode(token);
          // Check expiration
          if (decoded.exp * 1000 < Date.now()) {
            logout();
          } else {
            // Fetch fresh user data
            const res = await api.get('/auth/me');
            setUser(res.data);
          }
        } catch (error) {
          console.error("Invalid token:", error);
          logout();
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (username, password) => {
    try {
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);

      const res = await api.post('/auth/login', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });
      
      const token = res.data.access_token;
      localStorage.setItem('finance_ai_token', token);
      
      const userRes = await api.get('/auth/me');
      setUser(userRes.data);
      navigate('/dashboard');
      return { success: true };
    } catch (error) {
      const detail = error.response?.data?.detail;
      const message = Array.isArray(detail) ? detail[0].msg : (detail || "Login failed");
      return { success: false, message };
    }
  };

  const register = async (userData) => {
    try {
      await api.post('/auth/register', userData);
      // Automatically login after successful registration
      return await login(userData.username, userData.password);
    } catch (error) {
      const detail = error.response?.data?.detail;
      const message = Array.isArray(detail) ? detail[0].msg : (detail || "Registration failed");
      return { success: false, message };
    }
  };

  const logout = () => {
    localStorage.removeItem('finance_ai_token');
    setUser(null);
    navigate('/login');
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, setUser }}>
      {children}
    </AuthContext.Provider>
  );
};
