import React, { useState, useCallback, useRef } from 'react';
import { useNavigate } from 'react-router-dom';

import Orders from './Orders.jsx';
import VarietySelector from './VarietySelector.jsx';
import DeliveryDashboard from './DeliveryDashboard.jsx';
import SideMenu from './SideMenu.jsx';
import logo from '../assets/logo.svg';


const MainApp = ({ 
  dish, 
  setDish, 
  ingredients, 
  loading, 
  setLoading,
  error, 
  handleSubmit, 
 
  handleRecentSearchClick, 
  recentSearches, 
  user, 
  handleLogout,
  recipeInfo,
  servings,
  setServings,
  orders,
  addOrder
}) => {
  const inputRef = useRef(null);
  const navigate = useNavigate();
  const [showOrders, setShowOrders] = useState(false);
  const [showVarietySelector, setShowVarietySelector] = useState(false);
  const [showDeliveryDashboard, setShowDeliveryDashboard] = useState(false);
  const [isSideMenuOpen, setIsSideMenuOpen] = useState(false);

  const [varieties, setVarieties] = useState([]);

  const toggleSideMenu = () => {
    setIsSideMenuOpen(!isSideMenuOpen);
  };

  const closeSideMenu = () => {
    setIsSideMenuOpen(false);
  };

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

  return (
    <div className="App">
      <header className="App-header">
        <div className="user-info">
          <div className="logo" onClick={() => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
          }} style={{ cursor: 'pointer' }}>
            <img src={logo} alt="We Know Logo" className="landing-logo" />
          </div>
          <div className="header-right">
            <button className="orders-button" onClick={() => setShowOrders(true)}>
              🚚 My Deliveries
            </button>
            <button className="hamburger-menu-button" onClick={toggleSideMenu}>
              <div className="hamburger-icon">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </button>
          </div>
        </div>
        
        <div className="title-container">
          <div className="title-background">
            <h1 className="main-title">We Know</h1>
            <p className="title-subtitle">Get fresh ingredients delivered for any dish</p>
          </div>
        </div>
      </header>

      <main className="App-main">
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
                  disabled={loading}
                />
                
                <select
                  value={servings}
                  onChange={handleServingsChange}
                  className="servings-select"
                  disabled={loading}
                >
                  {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(num => (
                    <option key={num} value={num}>
                      {num} {num === 1 ? 'serving' : 'servings'}
                    </option>
                  ))}
                </select>
                
                <button type="submit" className="search-button" disabled={loading || !dish.trim()}>
                  {loading ? '🔍 Searching...' : '🔍 Find Ingredients'}
                </button>
                
                <button 
                  type="button" 
                  className="variety-button" 
                  onClick={handleSearchVarieties}
                  disabled={loading || !dish.trim()}
                >
                  🍽️ Show Varieties
                </button>
              </div>
            </form>

          {recentSearches.length > 0 && (
            <div className="recent-searches">
              <h3>Recent Searches:</h3>
              <div className="recent-tags">
                {recentSearches.map((search, index) => (
                  <button
                    key={index}
                    className="recent-tag"
                    onClick={() => handleRecentSearchClick(typeof search === 'string' ? search : search.dish)}
                                      >
                      {typeof search === 'string' ? search : search.dish}
                    </button>
                ))}
              </div>
            </div>
          )}
        </div>

        {error && (
          <div className="error-message">
            <p>{error}</p>
          </div>
        )}

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Searching for recipes...</p>
          </div>
        )}

        {ingredients && ingredients.length > 0 && recipeInfo && (
          <div className="results">
            <div className="recipe-info">
              <h2>📋 {recipeInfo.title}</h2>
              <p>
                Original recipe serves {recipeInfo.original_servings} people. 
                Scaled for {servings} {servings === 1 ? 'person' : 'people'}.
              </p>
            </div>

            <div className="ingredients-list">
              <h3>🛒 Grocery List</h3>
              <ul>
                {ingredients.map((ingredient, index) => {
                  const quantity = ingredient.quantity;
                  const unit = ingredient.unit || '';
                  const name = ingredient.ingredient || ingredient.name || ingredient.original || 'Unknown ingredient';
                  
                  return (
                    <li key={index} className="ingredient-item">
                      <span className="ingredient-amount">
                        {quantity !== null && quantity !== undefined ? `${quantity} ${unit}` : ''}
                      </span>
                      <span className="ingredient-name">{name}</span>
                    </li>
                  );
                })}
              </ul>
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

        {/* Side Menu */}
        <SideMenu
          user={user}
          isOpen={isSideMenuOpen}
          onClose={closeSideMenu}
          onLogout={handleLogout}
          onNavigateToProfile={() => {}}
          onNavigateToSettings={() => {}}
        />

      </main>
    </div>
  );
};

export default MainApp; 