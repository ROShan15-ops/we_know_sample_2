import React, { useState, useEffect } from 'react';
import './AlternativeIngredientsModal.css';

const AlternativeIngredientsModal = ({ 
  isOpen, 
  onClose, 
  alternativeSuggestions, 
  originalIngredients,
  onReplaceIngredients 
}) => {
  const [selectedAlternatives, setSelectedAlternatives] = useState({});
  const [showConfirmation, setShowConfirmation] = useState(false);
  const [activeTab, setActiveTab] = useState('allergens');

  // Prevent body scrolling when modal is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }

    // Cleanup function to restore body scrolling when component unmounts
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  if (!isOpen) return null;

  console.log('Modal opened - isOpen:', isOpen);
  console.log('Modal opened - alternativeSuggestions:', alternativeSuggestions);
  console.log('Modal opened - originalIngredients:', originalIngredients);
  
  // Debug: Log each allergen and its alternatives
  if (alternativeSuggestions) {
    Object.entries(alternativeSuggestions).forEach(([allergen, ingredientAlternatives]) => {
      console.log(`Allergen ${allergen}:`, ingredientAlternatives);
      Object.entries(ingredientAlternatives).forEach(([ingredient, alternatives]) => {
        console.log(`  ${ingredient} alternatives:`, alternatives);
      });
    });
  }

  const handleAlternativeSelect = (allergen, originalIngredient, alternative) => {
    setSelectedAlternatives(prev => ({
      ...prev,
      [originalIngredient]: alternative
    }));
  };

  const handleApplyChanges = () => {
    // Create new ingredients list with replacements
    const updatedIngredients = originalIngredients.map(ingredient => {
      const originalName = ingredient.ingredient;
      const replacement = selectedAlternatives[originalName];
      
      if (replacement) {
        return {
          ...ingredient,
          ingredient: replacement,
          original_ingredient: originalName, // Keep track of what was replaced
          is_replacement: true
        };
      }
      return ingredient;
    });

    onReplaceIngredients(updatedIngredients);
    setShowConfirmation(true);
    
    // Close modal after 2 seconds
    setTimeout(() => {
      setShowConfirmation(false);
      onClose();
      setSelectedAlternatives({});
    }, 2000);
  };

  const getIngredientQuantity = (originalName) => {
    const ingredient = originalIngredients.find(ing => ing.ingredient === originalName);
    return ingredient ? `${ingredient.quantity} ${ingredient.unit || ''}`.trim() : '';
  };

  const getAllergenIcon = (allergen) => {
    const icons = {
      dairy: '🥛',
      nuts: '🥜',
      gluten: '🌾',
      eggs: '🥚',
      shellfish: '🦐',
      soy: '🫘',
      fish: '🐟',
      wheat: '🌾'
    };
    return icons[allergen.toLowerCase()] || '⚠️';
  };

  const getAlternativeIcon = (alternative) => {
    if (alternative.includes('almond')) return '🥜';
    if (alternative.includes('coconut')) return '🥥';
    if (alternative.includes('soy')) return '🫘';
    if (alternative.includes('oat')) return '🌾';
    if (alternative.includes('rice')) return '🍚';
    if (alternative.includes('lemon')) return '🍋';
    if (alternative.includes('vinegar')) return '🍶';
    return '🔄';
  };

  return (
    <div className="alternative-modal-overlay">
      <div className="alternative-modal">
        <div className="alternative-modal-header">
          <div className="header-content">
            <div className="header-icon">🔄</div>
            <div className="header-text">
              <h2>Ingredient Alternatives</h2>
              <p>Make your recipe allergy-safe</p>
            </div>
          </div>
          <button className="close-btn" onClick={onClose}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        {showConfirmation ? (
          <div className="confirmation-message">
            <div className="confirmation-icon">✅</div>
            <h3>Ingredients Updated!</h3>
            <p>Your recipe has been updated with safe alternatives.</p>
            <div className="confirmation-progress">
              <div className="progress-bar"></div>
            </div>
          </div>
        ) : (
          <>
            <div className="alternative-modal-content">
              <div className="modal-tabs">
                <button 
                  className={`tab-btn ${activeTab === 'allergens' ? 'active' : ''}`}
                  onClick={() => setActiveTab('allergens')}
                >
                  <span className="tab-icon">⚠️</span>
                  Allergens
                </button>
                <button 
                  className={`tab-btn ${activeTab === 'summary' ? 'active' : ''}`}
                  onClick={() => setActiveTab('summary')}
                >
                  <span className="tab-icon">📋</span>
                  Summary
                </button>
              </div>

              {activeTab === 'allergens' && (
                <div className="allergens-content">
                  <div className="content-header">
                    <h3>Select Safe Alternatives</h3>
                    <p>Choose replacements for ingredients that contain allergens in your profile</p>
                  </div>

                  {Object.entries(alternativeSuggestions).map(([allergen, ingredientAlternatives]) => (
                      <div key={allergen} className="allergen-card">
                        <div className="allergen-header">
                          <span className="allergen-icon">{getAllergenIcon(allergen)}</span>
                          <div className="allergen-info">
                            <h4>{allergen.charAt(0).toUpperCase() + allergen.slice(1)} Allergy</h4>
                            <span className="allergen-count">
                              {Object.keys(ingredientAlternatives).length} ingredient{Object.keys(ingredientAlternatives).length !== 1 ? 's' : ''} to replace
                            </span>
                          </div>
                        </div>
                      
                      {Object.entries(ingredientAlternatives).map(([originalIngredient, alternatives]) => (
                        <div key={originalIngredient} className="ingredient-card">
                          <div className="original-ingredient">
                            <div className="original-info">
                              <span className="original-name">{originalIngredient}</span>
                              <span className="original-quantity">{getIngredientQuantity(originalIngredient)}</span>
                            </div>
                            <span className="original-badge">Original</span>
                          </div>
                          
                          <div className="alternatives-section">
                            <h5>Choose a replacement:</h5>
                            <div className="alternatives-grid">
                              {console.log(`Rendering ${alternatives.length} alternatives for ${originalIngredient}:`, alternatives)}
                              {alternatives.map((alternative, index) => {
                                console.log(`Rendering alternative ${index}:`, alternative);
                                return (
                                  <label key={index} className={`alternative-card ${selectedAlternatives[originalIngredient] === alternative ? 'selected' : ''}`}>
                                      <input
                                        type="radio"
                                        name={originalIngredient}
                                        value={alternative}
                                        checked={selectedAlternatives[originalIngredient] === alternative}
                                        onChange={() => handleAlternativeSelect(allergen, originalIngredient, alternative)}
                                      />
                                      <div className="alternative-content">
                                        <span className="alternative-icon">{getAlternativeIcon(alternative)}</span>
                                        <span className="alternative-text">{alternative}</span>
                                      </div>
                                      <div className="selection-indicator">
                                        <div className="radio-circle"></div>
                                      </div>
                                  </label>
                                );
                              })}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  ))}
                </div>
              )}

              {activeTab === 'summary' && (
                <div className="summary-content">
                  <div className="content-header">
                    <h3>Replacement Summary</h3>
                    <p>Review your selected alternatives before applying</p>
                  </div>

                  {Object.keys(selectedAlternatives).length === 0 ? (
                    <div className="empty-summary">
                      <div className="empty-icon">📝</div>
                      <h4>No replacements selected</h4>
                      <p>Go back to the Allergens tab to choose alternatives</p>
                    </div>
                  ) : (
                    <div className="replacements-list">
                      {Object.entries(selectedAlternatives).map(([original, replacement]) => (
                        <div key={original} className="replacement-item">
                          <div className="replacement-arrow">
                            <span className="original-text">{original}</span>
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                              <path d="M7 13l5 5 5-5"></path>
                              <path d="M7 6l5 5 5-5"></path>
                            </svg>
                            <span className="replacement-text">{replacement}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>

            <div className="alternative-modal-footer">
              <button className="cancel-btn" onClick={onClose}>
                Cancel
              </button>
              <button 
                className={`apply-btn ${Object.keys(selectedAlternatives).length > 0 ? 'active' : 'disabled'}`}
                onClick={handleApplyChanges}
                disabled={Object.keys(selectedAlternatives).length === 0}
              >
                <span className="btn-icon">✅</span>
                Apply Changes ({Object.keys(selectedAlternatives).length})
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default AlternativeIngredientsModal; 