import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AllergyManagementModal.css';

const AllergyManagementModal = ({ isOpen, onClose, user }) => {
  const [allergies, setAllergies] = useState([]);
  const [commonAllergens, setCommonAllergens] = useState([]);
  const [loading, setLoading] = useState(false);
  const [newAllergy, setNewAllergy] = useState('');
  const [customAllergy, setCustomAllergy] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Common allergens with emojis
  const allergenEmojis = {
    'peanuts': '🥜',
    'tree nuts': '🌰',
    'shellfish': '🦐',
    'fish': '🐟',
    'dairy': '🥛',
    'eggs': '🥚',
    'soy': '🫘',
    'wheat': '🌾',
    'gluten': '🌾',
    'sesame': '⚪',
    'sulfites': '🍷',
    'mustard': '🌶️',
    'celery': '🥬',
    'lupin': '🌱',
    'molluscs': '🐚'
  };

  useEffect(() => {
    if (isOpen) {
      setError(''); // Clear any previous errors when modal opens
      setSuccess(''); // Clear any previous success messages
      fetchUserAllergies();
      fetchCommonAllergens();
    }
  }, [isOpen]);

  // Clear error when allergies are successfully loaded
  useEffect(() => {
    if (allergies.length > 0 && error.includes('Please log in')) {
      setError('');
    }
  }, [allergies, error]);

  const fetchUserAllergies = async () => {
    try {
      setLoading(true);
      setError(''); // Clear any previous errors
      const token = localStorage.getItem('weKnowToken');
      
      if (!token) {
        setError('Please log in to manage your allergies');
        setAllergies([]); // Clear allergies if no token
        return;
      }
      
      const response = await axios.get('http://localhost:8000/user/allergies', {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      if (response.data.success) {
        setAllergies(response.data.allergies);
        // Clear error with a small delay to ensure UI updates
        setTimeout(() => setError(''), 100);
      } else {
        setError('Failed to load allergies');
        setAllergies([]);
      }
    } catch (error) {
      console.error('Error fetching allergies:', error);
      setAllergies([]); // Clear allergies on error
      if (error.response?.status === 401) {
        setError('Please log in to manage your allergies');
      } else {
        setError('Failed to load allergies. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const fetchCommonAllergens = async () => {
    try {
      const response = await axios.get('http://localhost:8000/allergies/common');
      if (response.data.success) {
        setCommonAllergens(response.data.allergens);
      }
    } catch (error) {
      console.error('Error fetching common allergens:', error);
    }
  };

  const addAllergy = async (allergyName, allergyType = 'common') => {
    try {
      setLoading(true);
      setError('');
      setSuccess('');
      
      const token = localStorage.getItem('weKnowToken');
      
      if (!token) {
        setError('Please log in to manage your allergies');
        return;
      }
      
      const response = await axios.post('http://localhost:8000/user/allergies', {
        allergy_name: allergyName,
        allergy_type: allergyType
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      if (response.data.success) {
        setSuccess(`Added ${allergyName} to your allergies`);
        setNewAllergy('');
        setCustomAllergy('');
        fetchUserAllergies(); // Refresh the list
      } else {
        setError(response.data.error || 'Failed to add allergy');
      }
    } catch (error) {
      console.error('Error adding allergy:', error);
      if (error.response?.status === 401) {
        setError('Please log in to manage your allergies');
      } else {
        setError(error.response?.data?.error || 'Failed to add allergy');
      }
    } finally {
      setLoading(false);
    }
  };

  const removeAllergy = async (allergyId, allergyName) => {
    if (!window.confirm(`Are you sure you want to remove ${allergyName} from your allergies?`)) {
      return;
    }

    try {
      setLoading(true);
      setError('');
      setSuccess('');
      
      const token = localStorage.getItem('weKnowToken');
      
      if (!token) {
        setError('Please log in to manage your allergies');
        return;
      }
      
      const response = await axios.delete(`http://localhost:8000/user/allergies/${allergyId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      if (response.data.success) {
        setSuccess(`Removed ${allergyName} from your allergies`);
        fetchUserAllergies(); // Refresh the list
      } else {
        setError(response.data.error || 'Failed to remove allergy');
      }
    } catch (error) {
      console.error('Error removing allergy:', error);
      if (error.response?.status === 401) {
        setError('Please log in to manage your allergies');
      } else {
        setError(error.response?.data?.error || 'Failed to remove allergy');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCommonAllergyClick = (allergen) => {
    const isAlreadyAdded = allergies.some(allergy => 
      allergy.allergy_name.toLowerCase() === allergen.toLowerCase()
    );
    
    if (isAlreadyAdded) {
      setError(`${allergen} is already in your allergies`);
      return;
    }
    
    addAllergy(allergen, 'common');
  };

  const handleCustomAllergySubmit = (e) => {
    e.preventDefault();
    if (!customAllergy.trim()) {
      setError('Please enter an allergy name');
      return;
    }
    
    const isAlreadyAdded = allergies.some(allergy => 
      allergy.allergy_name.toLowerCase() === customAllergy.toLowerCase()
    );
    
    if (isAlreadyAdded) {
      setError(`${customAllergy} is already in your allergies`);
      return;
    }
    
    addAllergy(customAllergy.trim(), 'custom');
  };

  const getEmoji = (allergyName) => {
    const lowerName = allergyName.toLowerCase();
    return allergenEmojis[lowerName] || '⚠️';
  };

  // Get token using the correct key
  const token = localStorage.getItem('weKnowToken');
  const isAuthenticated = !!token;

  if (!isOpen) return null;

  return (
    <div className="allergy-modal-overlay" onClick={onClose}>
      <div className="allergy-modal" onClick={(e) => e.stopPropagation()} key={isOpen ? 'open' : 'closed'}>
        {/* Header */}
        <div className="allergy-modal-header">
          <div className="allergy-modal-title">
            <span className="allergy-icon">⚠️</span>
            <div>
              <h2>Manage Allergies</h2>
              <p>Keep your allergy profile updated for safer food recommendations</p>
            </div>
          </div>
          <button className="close-button" onClick={onClose}>✕</button>
        </div>

        {/* Content */}
        <div className="allergy-modal-content">
          {/* Error/Success Messages */}
          {error && (
            <div className="message error">
              <span>❌</span> {error}
            </div>
          )}
          {success && (
            <div className="message success">
              <span>✅</span> {success}
            </div>
          )}

          {!isAuthenticated ? (
            /* Login Required Section */
            <div className="login-required-section">
              <div className="login-required-content">
                <span className="login-icon">🔐</span>
                <h3>Login Required</h3>
                <p>Please log in to manage your allergy profile and get personalized food recommendations.</p>
                <div className="login-benefits">
                  <div className="benefit-item">
                    <span className="benefit-icon">⚠️</span>
                    <span>Track your allergies</span>
                  </div>
                  <div className="benefit-item">
                    <span className="benefit-icon">🔄</span>
                    <span>Get safe alternatives</span>
                  </div>
                  <div className="benefit-item">
                    <span className="benefit-icon">🍽️</span>
                    <span>Personalized recommendations</span>
                  </div>
                </div>
                <button className="login-button" onClick={onClose}>
                  Close & Login
                </button>
              </div>
            </div>
          ) : (
            /* Authenticated Content */
            <>
              {/* Current Allergies */}
              <div className="section">
                <h3>Your Current Allergies</h3>
                {loading ? (
                  <div className="loading">Loading...</div>
                ) : allergies.length === 0 ? (
                  <div className="empty-state">
                    <span className="empty-icon">📝</span>
                    <p>No allergies added yet</p>
                    <p className="empty-subtitle">Add your allergies below to get personalized recommendations</p>
                  </div>
                ) : (
                  <div className="allergies-list">
                    {allergies.map((allergy) => (
                      <div key={allergy.id} className="allergy-item">
                        <div className="allergy-info">
                          <span className="allergy-emoji">{getEmoji(allergy.allergy_name)}</span>
                          <span className="allergy-name">{allergy.allergy_name}</span>
                          <span className="allergy-type">{allergy.allergy_type}</span>
                        </div>
                        <button 
                          className="remove-button"
                          onClick={() => removeAllergy(allergy.id, allergy.allergy_name)}
                          disabled={loading}
                        >
                          ✕
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Add Common Allergies */}
              <div className="section">
                <h3>Add Common Allergies</h3>
                <p className="section-subtitle">Click on any allergy to add it to your profile</p>
                <div className="common-allergens-grid">
                  {commonAllergens.map((allergen) => {
                    const isAdded = allergies.some(allergy => 
                      allergy.allergy_name.toLowerCase() === allergen.toLowerCase()
                    );
                    return (
                      <button
                        key={allergen}
                        className={`allergen-chip ${isAdded ? 'added' : ''}`}
                        onClick={() => handleCommonAllergyClick(allergen)}
                        disabled={isAdded || loading}
                      >
                        <span className="allergen-emoji">{getEmoji(allergen)}</span>
                        <span className="allergen-text">{allergen}</span>
                        {isAdded && <span className="added-check">✓</span>}
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Add Custom Allergy */}
              <div className="section">
                <h3>Add Custom Allergy</h3>
                <p className="section-subtitle">Add any allergy not listed above</p>
                <form onSubmit={handleCustomAllergySubmit} className="custom-allergy-form">
                  <div className="input-group">
                    <input
                      type="text"
                      value={customAllergy}
                      onChange={(e) => setCustomAllergy(e.target.value)}
                      placeholder="Enter allergy name (e.g., kiwi, mango)"
                      className="custom-allergy-input"
                      disabled={loading}
                    />
                    <button 
                      type="submit" 
                      className="add-button"
                      disabled={!customAllergy.trim() || loading}
                    >
                      Add
                    </button>
                  </div>
                </form>
              </div>
            </>
          )}
        </div>

        {/* Footer */}
        <div className="allergy-modal-footer">
          {isAuthenticated ? (
            <button className="done-button" onClick={onClose}>
              Done
            </button>
          ) : (
            <button className="done-button" onClick={onClose}>
              Close
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default AllergyManagementModal; 