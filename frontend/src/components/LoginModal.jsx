import React, { useState, useEffect, useCallback, useRef } from 'react';
import axios from 'axios';

const LoginModal = ({ isOpen, onClose, onLogin }) => {
  const [loginData, setLoginData] = useState({ email: '', password: '' });
  const [authError, setAuthError] = useState('');
  const emailRef = useRef(null);
  const passwordRef = useRef(null);

  useEffect(() => {
    if (isOpen && emailRef.current) {
      setTimeout(() => {
        emailRef.current.focus();
      }, 100);
    }
  }, [isOpen]);

  const handleEmailChange = useCallback((e) => {
    setLoginData(prev => ({...prev, email: e.target.value}));
  }, []);

  const handlePasswordChange = useCallback((e) => {
    setLoginData(prev => ({...prev, password: e.target.value}));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setAuthError('');
    
    if (!loginData.email || !loginData.password) {
      setAuthError('Please fill in all fields');
      return;
    }

    try {
              const response = await axios.post('http://localhost:8000/auth/login', {
        email: loginData.email,
        password: loginData.password
      });

      if (response.data.success) {
        localStorage.setItem('weKnowToken', response.data.access_token);
        localStorage.setItem('weKnowUser', JSON.stringify(response.data.user));
        onLogin();
        setLoginData({ email: '', password: '' });
      } else {
        setAuthError(response.data.error || 'Login failed');
      }
    } catch (err) {
      console.error('Login error:', err);
      if (err.response?.data?.error) {
        setAuthError(err.response.data.error);
      } else {
        setAuthError('Failed to connect to the server. Please try again.');
      }
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" key="login-modal">
      <div className="auth-modal">
        <button className="close-button" onClick={onClose}>×</button>
        <h2>Login</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <input
              type="email"
              placeholder="Email"
              value={loginData.email}
              onChange={handleEmailChange}
              required
              autoComplete="email"
              ref={emailRef}
            />
          </div>
          <div className="form-group">
            <input
              type="password"
              placeholder="Password"
              value={loginData.password}
              onChange={handlePasswordChange}
              required
              autoComplete="current-password"
              ref={passwordRef}
            />
          </div>
          {authError && <div className="auth-error">{authError}</div>}
          <button type="submit" className="auth-submit-button">Login</button>
        </form>
      </div>
    </div>
  );
};

export default LoginModal; 