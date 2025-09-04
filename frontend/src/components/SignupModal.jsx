import React, { useState, useEffect, useCallback, useRef } from 'react';
import axios from 'axios';

const SignupModal = ({ isOpen, onClose, onSignup }) => {
  const [signupData, setSignupData] = useState({ name: '', email: '', password: '', confirmPassword: '' });
  const [selectedAllergies, setSelectedAllergies] = useState([]);
  const [customAllergy, setCustomAllergy] = useState('');
  const [commonAllergens, setCommonAllergens] = useState([]);
  const [currentStep, setCurrentStep] = useState(1);
  const [authError, setAuthError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const nameRef = useRef(null);
  const emailRef = useRef(null);
  const passwordRef = useRef(null);
  const confirmPasswordRef = useRef(null);

  useEffect(() => {
    if (isOpen && nameRef.current) {
      setTimeout(() => {
        nameRef.current.focus();
      }, 100);
    }
  }, [isOpen]);

  // Fetch common allergens when modal opens
  useEffect(() => {
    if (isOpen) {
      fetchCommonAllergens();
    }
  }, [isOpen]);

  const fetchCommonAllergens = async () => {
    try {
      const response = await axios.get('http://localhost:8000/allergies/common');
      if (response.data.success) {
        setCommonAllergens(response.data.allergens);
      }
    } catch (error) {
      console.error('Failed to fetch common allergens:', error);
    }
  };

  const handleNameChange = useCallback((e) => {
    setSignupData(prev => ({...prev, name: e.target.value}));
  }, []);

  const handleEmailChange = useCallback((e) => {
    setSignupData(prev => ({...prev, email: e.target.value}));
  }, []);

  const handlePasswordChange = useCallback((e) => {
    setSignupData(prev => ({...prev, password: e.target.value}));
  }, []);

  const handleConfirmPasswordChange = useCallback((e) => {
    setSignupData(prev => ({...prev, confirmPassword: e.target.value}));
  }, []);

  const handleAllergyToggle = (allergy) => {
    setSelectedAllergies(prev => 
      prev.includes(allergy) 
        ? prev.filter(a => a !== allergy)
        : [...prev, allergy]
    );
  };

  const handleCustomAllergyAdd = () => {
    if (customAllergy.trim() && !selectedAllergies.includes(customAllergy.trim())) {
      setSelectedAllergies(prev => [...prev, customAllergy.trim()]);
      setCustomAllergy('');
    }
  };

  const handleCustomAllergyRemove = (allergy) => {
    setSelectedAllergies(prev => prev.filter(a => a !== allergy));
  };

  const handleNextStep = () => {
    if (currentStep === 1) {
      if (!signupData.name || !signupData.email || !signupData.password || !signupData.confirmPassword) {
        setAuthError('Please fill in all fields');
        return;
      }
      if (signupData.password !== signupData.confirmPassword) {
        setAuthError('Passwords do not match');
        return;
      }
      if (signupData.password.length < 6) {
        setAuthError('Password must be at least 6 characters');
        return;
      }
      setCurrentStep(2);
      setAuthError('');
    }
  };

  const handlePrevStep = () => {
    setCurrentStep(1);
    setAuthError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setAuthError('');
    setIsLoading(true);
    
    try {
      const response = await axios.post('http://localhost:8000/auth/register', {
        name: signupData.name,
        email: signupData.email,
        password: signupData.password,
        allergies: selectedAllergies
      });

      if (response.data.success) {
        localStorage.setItem('weKnowToken', response.data.access_token);
        localStorage.setItem('weKnowUser', JSON.stringify(response.data.user));
        onSignup();
        setSignupData({ name: '', email: '', password: '', confirmPassword: '' });
        setSelectedAllergies([]);
        setCurrentStep(1);
      } else {
        setAuthError(response.data.error || 'Registration failed');
      }
    } catch (err) {
      console.error('Registration error:', err);
      if (err.response?.data?.error) {
        setAuthError(err.response.data.error);
      } else {
        setAuthError('Failed to connect to the server. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;



  return (
    <div className="modal-overlay" key="signin-modal">
      <div className="auth-modal">
        <button className="close-button" onClick={onClose}>×</button>
        <h2>Sign Up</h2>
        
        {/* Step indicator */}
        <div className="step-indicator">
          <div className={`step ${currentStep >= 1 ? 'active' : ''}`}>1. Account</div>
          <div className={`step ${currentStep >= 2 ? 'active' : ''}`}>2. Allergies</div>
        </div>
        


        {currentStep === 1 && (
          <form onSubmit={(e) => { e.preventDefault(); }}>
            <div className="form-group">
              <input
                type="text"
                placeholder="Full Name"
                value={signupData.name}
                onChange={handleNameChange}
                required
                autoComplete="name"
                ref={nameRef}
              />
            </div>
            <div className="form-group">
              <input
                type="email"
                placeholder="Email"
                value={signupData.email}
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
                value={signupData.password}
                onChange={handlePasswordChange}
                required
                autoComplete="new-password"
                ref={passwordRef}
              />
            </div>
            <div className="form-group">
              <input
                type="password"
                placeholder="Confirm Password"
                value={signupData.confirmPassword}
                onChange={handleConfirmPasswordChange}
                required
                autoComplete="new-password"
                ref={confirmPasswordRef}
              />
            </div>
            {authError && <div className="auth-error">{authError}</div>}
            <button type="button" onClick={handleNextStep} className="auth-submit-button">Next: Allergies</button>
          </form>
        )}

        {currentStep === 2 && (
          <form onSubmit={handleSubmit}>
            <div className="allergy-section">
              <h3>Select Your Allergies (Optional)</h3>
              <p className="allergy-description">
                Help us keep you safe by selecting any food allergies you have. 
                We'll warn you about dishes containing these ingredients.
              </p>
              
              {/* Common Allergens */}
              <div className="allergy-group">
                <h4>Common Allergens</h4>
                <div className="allergy-checkboxes">
                  {commonAllergens.length > 0 ? (
                    commonAllergens.map((allergy) => (
                      <label key={allergy} className="allergy-checkbox">
                        <input
                          type="checkbox"
                          checked={selectedAllergies.includes(allergy)}
                          onChange={() => handleAllergyToggle(allergy)}
                        />
                        <span>{allergy}</span>
                      </label>
                    ))
                  ) : (
                    <div className="loading-allergens">
                      <p>Loading common allergens...</p>
                      {/* Fallback allergens in case API fails */}
                      {['peanuts', 'tree nuts', 'shellfish', 'dairy', 'eggs'].map((allergy) => (
                        <label key={allergy} className="allergy-checkbox">
                          <input
                            type="checkbox"
                            checked={selectedAllergies.includes(allergy)}
                            onChange={() => handleAllergyToggle(allergy)}
                          />
                          <span>{allergy}</span>
                        </label>
                      ))}
                    </div>
                  )}
                </div>
              </div>

              {/* Custom Allergies */}
              <div className="allergy-group">
                <h4>Custom Allergies</h4>
                <div className="custom-allergy-input">
                  <input
                    type="text"
                    placeholder="Add custom allergy (e.g., kiwi, mango)"
                    value={customAllergy}
                    onChange={(e) => setCustomAllergy(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleCustomAllergyAdd())}
                  />
                  <button 
                    type="button" 
                    onClick={handleCustomAllergyAdd}
                    className="add-allergy-btn"
                  >
                    Add
                  </button>
                </div>
                
                {/* Selected Custom Allergies */}
                {selectedAllergies.filter(a => !commonAllergens.includes(a)).length > 0 && (
                  <div className="selected-custom-allergies">
                    {selectedAllergies
                      .filter(allergy => !commonAllergens.includes(allergy))
                      .map((allergy) => (
                        <span key={allergy} className="allergy-tag">
                          {allergy}
                          <button 
                            type="button" 
                            onClick={() => handleCustomAllergyRemove(allergy)}
                            className="remove-allergy-btn"
                          >
                            ×
                          </button>
                        </span>
                      ))}
                  </div>
                )}
              </div>

              {/* Selected Allergies Summary */}
              {selectedAllergies.length > 0 && (
                <div className="selected-allergies-summary">
                  <h4>Your Allergies:</h4>
                  <div className="allergy-tags">
                    {selectedAllergies.map((allergy) => (
                      <span key={allergy} className="allergy-tag">
                        {allergy}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {authError && <div className="auth-error">{authError}</div>}
            <div className="auth-buttons">
              <button type="button" onClick={handlePrevStep} className="auth-back-button">
                Back
              </button>
              <button type="submit" className="auth-submit-button" disabled={isLoading}>
                {isLoading ? 'Creating Account...' : 'Create Account'}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};

export default SignupModal; 