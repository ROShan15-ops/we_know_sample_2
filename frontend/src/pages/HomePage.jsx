import React, { useCallback, useRef, useState } from 'react';

import Orders from '../components/Orders.jsx';
import VarietySelector from '../components/VarietySelector.jsx';
import DeliveryDashboard from '../components/DeliveryDashboard.jsx';
import AlternativeIngredientsModal from '../components/AlternativeIngredientsModal.jsx';

const HomePage = ({ 
  dish, 
  setDish, 
  ingredients, 
  loading, 
  setLoading,
  error, 
  setError,
  successMessage,
  setSuccessMessage,
  handleSubmit, 
 
  handleRecentSearchClick, 
  recentSearches, 
  recipeInfo,
  nutritionInfo,
  allergyWarning,
  alternativeSuggestions,
  servings,
  setServings,
  orders,
  addOrder,
  deleteIngredient, // Add this new prop
  onReplaceIngredients // Add this new prop
}) => {
  const inputRef = useRef(null);
  const [showOrders, setShowOrders] = useState(false);
  const [showVarietySelector, setShowVarietySelector] = useState(false);
  const [showDeliveryDashboard, setShowDeliveryDashboard] = useState(false);
  const [showAlternativeIngredientsModal, setShowAlternativeIngredientsModal] = useState(false);
  const [currentIngredients, setCurrentIngredients] = useState([]);

  const [varieties, setVarieties] = useState([]);

  // Debug logging
  console.log('HomePage Debug:', {
    dish,
    ingredients: ingredients?.length,
    loading,
    error,
    recipeInfo: !!recipeInfo,
    recentSearches: recentSearches?.length
  });

  const handleInputChange = useCallback((e) => {
    setDish(e.target.value);
  }, [setDish]);

  const handleServingsChange = useCallback((e) => {
    setServings(parseInt(e.target.value));
  }, [setServings]);

  const handleVarietySelect = async (variety) => {
    setShowVarietySelector(false);
    
    // Update the dish name in the parent component
    setDish(variety.title);
    
    // Call handleSubmit directly with the variety title
    handleSubmit({ preventDefault: () => {} }, variety.title);
  };

  const handleSearchVarieties = async () => {
    if (!dish.trim()) return;
    
    try {
      const response = await fetch('http://localhost:8000/search-varieties', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('weKnowToken')}`
        },
        body: JSON.stringify({ dish_name: dish })
      });
      
      const data = await response.json();
      
      if (data.success && data.varieties.length > 0) {
        setVarieties(data.varieties);
        setShowVarietySelector(true);
      } else {
        // If no varieties found, proceed with normal search
        handleSubmit({ preventDefault: () => {} });
      }
    } catch (error) {
      console.error('Error searching varieties:', error);
      // Fallback to normal search
      handleSubmit({ preventDefault: () => {} });
    }
  };

  const handleOpenAlternativeModal = () => {
    setCurrentIngredients(ingredients);
    setShowAlternativeIngredientsModal(true);
  };

  const handleReplaceIngredients = (updatedIngredients) => {
    // Update the ingredients in the parent component
    // This will need to be passed down from App.jsx
    if (typeof onReplaceIngredients === 'function') {
      onReplaceIngredients(updatedIngredients);
    }
  };

  return (
    <div className="home-page">
      {/* Debug Info */}
      <div style={{ 
        background: '#f0f0f0', 
        padding: '10px', 
        margin: '10px', 
        borderRadius: '5px',
        fontSize: '12px',
        fontFamily: 'monospace'
      }}>
        <strong>Debug Info:</strong><br/>
        Dish: "{dish}"<br/>
        Ingredients: {ingredients?.length || 0}<br/>
        Loading: {loading ? 'Yes' : 'No'}<br/>
        Error: {error || 'None'}<br/>
        Recipe Info: {recipeInfo ? 'Yes' : 'No'}<br/>
        Recent Searches: {recentSearches?.length || 0}
      </div>

      <div className="search-section">
        <form onSubmit={handleSubmit} className="search-form">
          <div className="input-group">
            <input
              type="text"
              value={dish}
              onChange={handleInputChange}
              placeholder="Enter a dish name (e.g., Chicken Tikka Masala, Spaghetti Carbonara)"
              className="dish-input"
              ref={inputRef}
              autoFocus
            />
            <select
              value={servings}
              onChange={handleServingsChange}
              className="servings-select"
            >
              {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(num => (
                <option key={num} value={num}>
                  {num} {num === 1 ? 'serving' : 'servings'}
                </option>
              ))}
            </select>
            <button type="submit" className="search-button" disabled={loading}>
              {loading ? '🔍 Searching...' : '🔍 Find Ingredients'}
            </button>
            <button 
              type="button" 
              className="variety-button"
              onClick={handleSearchVarieties}
              disabled={loading}
            >
              📷 Show Varieties
            </button>
          </div>
        </form>

        {/* Recent Searches */}
        {recentSearches.length > 0 && (
          <div className="recent-searches">
            <h3>Recent Searches:</h3>
            <ul className="recent-tags">
              {recentSearches.map((search, index) => (
                <li key={index}>
                  <button
                    className="recent-tag"
                    onClick={() => handleRecentSearchClick(typeof search === 'string' ? search : search.dish)}
                  >
                    {typeof search === 'string' ? search : search.dish}
                  </button>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Searching for ingredients...</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="error-message">
            <h3>❌ No Ingredients Found</h3>
            <p>{error}</p>
            <div className="error-suggestions">
              <h4>💡 Try these alternatives:</h4>
              <div className="suggestion-buttons">
                <button 
                  onClick={() => {
                    setDish('Chicken Tikka Masala');
                    setError('');
                  }}
                  className="suggestion-btn"
                >
                  Chicken Tikka Masala
                </button>
                <button 
                  onClick={() => {
                    setDish('Spaghetti Carbonara');
                    setError('');
                  }}
                  className="suggestion-btn"
                >
                  Spaghetti Carbonara
                </button>
                <button 
                  onClick={() => {
                    setDish('Margherita Pizza');
                    setError('');
                  }}
                  className="suggestion-btn"
                >
                  Margherita Pizza
                </button>
                <button 
                  onClick={() => {
                    setDish('Butter Chicken');
                    setError('');
                  }}
                  className="suggestion-btn"
                >
                  Butter Chicken
                </button>
                <button 
                  onClick={() => {
                    setDish('Pasta Bolognese');
                    setError('');
                  }}
                  className="suggestion-btn"
                >
                  Pasta Bolognese
                </button>
              </div>
              <p className="error-tip">
                <strong>Tip:</strong> Try using more common dish names or English translations. 
                Regional dishes might not be available in our database.
              </p>
            </div>
            <button 
              onClick={() => {
                setError('');
                setDish('');
              }} 
              className="clear-error-btn"
            >
              Clear & Try Again
            </button>
          </div>
        )}

        {/* Success Message */}
        {successMessage && (
          <div className="success-message">
            <h3>🎉 {successMessage}</h3>
          </div>
        )}

        {/* Results */}
        {ingredients && ingredients.length > 0 && recipeInfo && (
          <div className="results">
            {/* Debug: Log ingredients to console */}
            {console.log('DEBUG - Ingredients received:', ingredients)}
            
            <div className="recipe-info">
              <h2>📋 {recipeInfo.title}</h2>
              <p>
                Original recipe serves {recipeInfo.original_servings} people. 
                Scaled for {servings} {servings === 1 ? 'person' : 'people'}.
              </p>
            </div>

            {/* Allergy Warning */}
            {allergyWarning && (
              <div className="allergy-warning">
                <h3>⚠️ Allergy Alert</h3>
                <p>{allergyWarning}</p>
                {alternativeSuggestions && Object.keys(alternativeSuggestions).length > 0 && (
                  <button 
                    className="view-alternatives-btn"
                    onClick={handleOpenAlternativeModal}
                  >
                    🔄 View Alternative Ingredients
                  </button>
                )}
              </div>
            )}



            {/* Nutrition Information */}
            {nutritionInfo && (
              <div className="nutrition-info">
                <h3>🍎 Nutrition Facts</h3>
                <div className="nutrition-grid">
                  <div className="nutrition-item">
                    <span className="nutrition-label">Calories</span>
                    <span className="nutrition-value">
                      {nutritionInfo.calories !== "unknown" ? `${nutritionInfo.calories} kcal` : "Unknown"}
                    </span>
                  </div>
                  <div className="nutrition-item">
                    <span className="nutrition-label">Protein</span>
                    <span className="nutrition-value">
                      {nutritionInfo.protein !== "unknown" ? `${nutritionInfo.protein}g` : "Unknown"}
                    </span>
                  </div>
                  <div className="nutrition-item">
                    <span className="nutrition-label">Carbs</span>
                    <span className="nutrition-value">
                      {nutritionInfo.carbs !== "unknown" ? `${nutritionInfo.carbs}g` : "Unknown"}
                    </span>
                  </div>
                  <div className="nutrition-item">
                    <span className="nutrition-label">Fat</span>
                    <span className="nutrition-value">
                      {nutritionInfo.fat !== "unknown" ? `${nutritionInfo.fat}g` : "Unknown"}
                    </span>
                  </div>
                  {nutritionInfo.fiber !== "unknown" && (
                    <div className="nutrition-item">
                      <span className="nutrition-label">Fiber</span>
                      <span className="nutrition-value">{nutritionInfo.fiber}g</span>
                    </div>
                  )}
                  {nutritionInfo.sugar !== "unknown" && (
                    <div className="nutrition-item">
                      <span className="nutrition-label">Sugar</span>
                      <span className="nutrition-value">{nutritionInfo.sugar}g</span>
                    </div>
                  )}
                </div>
                
                {/* Dietary Tags */}
                {nutritionInfo.dietary_tags && nutritionInfo.dietary_tags.length > 0 && (
                  <div className="dietary-tags">
                    <h4>Dietary Information:</h4>
                    <div className="tags-container">
                      {nutritionInfo.dietary_tags.map((tag, index) => (
                        <span key={index} className="dietary-tag">
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            <div className="ingredients-list">
              <h3>🛒 Grocery List</h3>
              <div className="ingredients-grid">
                {ingredients.map((ingredient, index) => {
                  const quantity = ingredient.quantity;
                  const unit = ingredient.unit || '';
                  let name = ingredient.ingredient || ingredient.name || ingredient.original || 'Unknown ingredient';
                  
                  // Debug: Log each ingredient name
                  {console.log(`DEBUG - Ingredient ${index}:`, name)}
                  
                  // Clean up the name
                  name = name.replace(/\s+/g, ' ').trim();
                  
                  // Generate ingredient image URL using Unsplash API
                  const imageUrl = `https://source.unsplash.com/300x200/?${encodeURIComponent(name)}`;
                  
                  return (
                    <div 
                      key={index} 
                      className="ingredient-card"
                      style={{ animationDelay: `${index * 0.1}s` }}
                    >
                      <div className="ingredient-image">
                        <img 
                          src={imageUrl} 
                          alt={name}
                          loading="lazy"
                          onLoad={(e) => {
                            e.target.style.opacity = '1';
                            e.target.parentElement.querySelector('.image-loading').style.display = 'none';
                          }}
                          onError={(e) => {
                            e.target.src = `https://source.unsplash.com/300x200/?food,${encodeURIComponent(name.split(' ')[0])}`;
                            // If the fallback also fails, show a placeholder
                            e.target.onerror = () => {
                              e.target.style.display = 'none';
                              e.target.parentElement.querySelector('.image-loading').innerHTML = 
                                `<div style="display: flex; align-items: center; justify-content: center; height: 100%; color: #999; font-size: 14px;">
                                  🥘 ${name}
                                </div>`;
                            };
                          }}
                          style={{ opacity: 0, transition: 'opacity 0.3s ease' }}
                        />
                        <div className="image-loading">
                          <div className="loading-spinner"></div>
                        </div>
                      </div>
                      <div className="ingredient-details">
                        <h4 className="ingredient-name">{name}</h4>
                        <p className="ingredient-amount">
                          {quantity !== null && quantity !== undefined ? `${quantity} ${unit}` : 'As needed'}
                        </p>
                        <button 
                          className="delete-ingredient-btn" 
                          onClick={() => deleteIngredient(index)}
                          title="Remove ingredient"
                        >
                          ✕
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            <div className="action-buttons">
              <button 
                className="action-button delivery-button" 
                onClick={() => setShowDeliveryDashboard(true)}
                style={{
                  background: 'linear-gradient(135deg, #27ae60, #229954)',
                  color: 'white',
                  border: 'none',
                  padding: '12px 24px',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  fontSize: '14px',
                  fontWeight: '600',
                  transition: 'all 0.3s ease'
                }}
              >
                🚚 Get Ingredients Delivered
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Orders Modal */}
      {showOrders && (
        <Orders
          orders={orders}
          onClose={() => setShowOrders(false)}
        />
      )}

      {/* Variety Selector Modal */}
      {showVarietySelector && (
        <VarietySelector
          varieties={varieties}
          onSelectVariety={handleVarietySelect}
          onClose={() => setShowVarietySelector(false)}
        />
      )}

      {/* Delivery Dashboard Modal */}
      {showDeliveryDashboard && (
        <DeliveryDashboard
          onClose={() => setShowDeliveryDashboard(false)}
          selectedDish={dish}
          selectedServings={servings}
          addOrder={addOrder}
        />
      )}

      {/* Alternative Ingredients Modal */}
      {showAlternativeIngredientsModal && (
        <AlternativeIngredientsModal
          isOpen={showAlternativeIngredientsModal}
          onClose={() => setShowAlternativeIngredientsModal(false)}
          alternativeSuggestions={alternativeSuggestions}
          originalIngredients={currentIngredients}
          onReplaceIngredients={handleReplaceIngredients}
        />
      )}
    </div>
  );
};

export default HomePage; 