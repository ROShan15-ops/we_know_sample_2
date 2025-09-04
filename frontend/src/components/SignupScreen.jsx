import React, { useState } from 'react';
import axios from 'axios';
import './SignupScreen.css';

const SignupScreen = ({ onSwitchToLogin, onSignupSuccess }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email';
    }
    
    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }
    
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    setIsLoading(true);
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Call the backend registration API
      const response = await axios.post('http://localhost:8000/auth/register', {
        name: formData.email.split('@')[0],
        email: formData.email,
        password: formData.password
      });
      
      if (response.data.success) {
        // Store the real token and user data
        localStorage.setItem('weKnowToken', response.data.access_token);
        localStorage.setItem('weKnowUser', JSON.stringify(response.data.user));
        
        onSignupSuccess(response.data.user);
      } else {
        throw new Error(response.data.error || 'Registration failed');
      }
    } catch (error) {
      setErrors({ general: 'Signup failed. Please try again.' });
    } finally {
      setIsLoading(false);
    }
  };



  return (
    <div className="signup-screen">
      <div className="signup-container">
        {/* Header */}
        <div className="signup-header">
          <h1>Create Account</h1>
          <p>Join us to discover amazing recipes and ingredients</p>
        </div>



        {/* Email/Password Form */}
        <form className="signup-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              placeholder="Enter your email"
              className={errors.email ? 'error' : ''}
            />
            {errors.email && <span className="error-message">{errors.email}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              placeholder="Create a password"
              className={errors.password ? 'error' : ''}
            />
            {errors.password && <span className="error-message">{errors.password}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password</label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleInputChange}
              placeholder="Confirm your password"
              className={errors.confirmPassword ? 'error' : ''}
            />
            {errors.confirmPassword && <span className="error-message">{errors.confirmPassword}</span>}
          </div>

          {errors.general && (
            <div className="error-message general-error">{errors.general}</div>
          )}

          <button 
            type="submit" 
            className="signup-btn"
            disabled={isLoading}
          >
            {isLoading ? (
              <div className="loading-spinner">
                <div className="spinner"></div>
                Creating Account...
              </div>
            ) : (
              'Sign Up'
            )}
          </button>
        </form>

        {/* Login Link */}
        <div className="login-link">
          <p>
            Already have an account?{' '}
            <button 
              type="button" 
              className="link-btn"
              onClick={onSwitchToLogin}
            >
              Log in
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

export default SignupScreen; 