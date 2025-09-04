import React, { useState, useEffect, useRef } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import axios from 'axios';
import './App.css';
import userDataService from './services/userDataService';
import { clearAllLocalStorage, logLocalStorageData } from './utils/clearLocalStorage';

// Import components
import { LoginModal, SignupModal, LandingPage, SignupScreen } from './components';
import AppLayout from './components/AppLayout.jsx';

// Import pages
import HomePage from './pages/HomePage';
import OrderHistory from './pages/OrderHistory';
import SavedAddresses from './pages/SavedAddresses';
import Settings from './pages/Settings';
import TrackOrders from './pages/TrackOrders';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [showLoginForm, setShowLoginForm] = useState(false);
  const [showSignupScreen, setShowSignupScreen] = useState(false);
  const [isLoadingUserData, setIsLoadingUserData] = useState(false);
  const [dishName, setDishName] = useState('');
  const [servings, setServings] = useState(2);
  const [ingredients, setIngredients] = useState([]);
  const [recipeInfo, setRecipeInfo] = useState(null);
  const [nutritionInfo, setNutritionInfo] = useState(null);
  const [allergyWarning, setAllergyWarning] = useState(null);
  const [alternativeSuggestions, setAlternativeSuggestions] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const [recentSearches, setRecentSearches] = useState([]);
  const [orders, setOrders] = useState([]);

  // Debug logging for authentication state
  console.log('App Debug - isAuthenticated:', isAuthenticated);
  console.log('App Debug - showLoginForm:', showLoginForm);
  console.log('App Debug - showSignupScreen:', showSignupScreen);

  // Function to navigate to landing page (home)
  const navigateToHome = () => {
    console.log('navigateToHome called - setting isAuthenticated to false');
    setIsAuthenticated(false);
    setShowLoginForm(false);
    setShowSignupScreen(false);
    // Clear any authentication data
    localStorage.removeItem('weKnowToken');
    localStorage.removeItem('weKnowUser');
    localStorage.removeItem('weKnowOrders');
    localStorage.removeItem('weKnowRecentSearches');
    // Scroll to top of the page
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };
  
  // Load recent searches from database on component mount
  useEffect(() => {
    const loadRecentSearches = async () => {
      if (isAuthenticated) {
        try {
          const searches = await userDataService.getRecentSearches();
          setRecentSearches(searches.map(search => search.dish_name));
        } catch (error) {
          console.error('Error loading recent searches:', error);
        }
      } else {
        // Clear local state when not authenticated
        setRecentSearches([]);
      }
    };
    
    loadRecentSearches();
  }, [isAuthenticated]);

  // Load orders from database when authenticated
  useEffect(() => {
    const loadOrders = async () => {
      if (isAuthenticated) {
        try {
          const userOrders = await userDataService.getOrders();
          setOrders(userOrders);
          // No longer saving to localStorage - components will fetch from database
        } catch (error) {
          console.error('Error loading orders:', error);
        }
      } else {
        // Clear local state when not authenticated
        setOrders([]);
      }
    };
    
    loadOrders();
  }, [isAuthenticated]);

  // Function to refresh orders
  const refreshOrders = async () => {
    if (isAuthenticated) {
      try {
        const userOrders = await userDataService.getOrders();
        setOrders(userOrders);
      } catch (error) {
        console.error('Error refreshing orders:', error);
      }
    }
  };

  // Check if user is already authenticated
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('weKnowToken');
      if (token) {
        try {
          // Verify token with backend
          const response = await axios.get('http://localhost:8000/auth/me', {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          
          if (response.data.success) {
            setIsAuthenticated(true);
            // Clear any old localStorage data that might interfere
            localStorage.removeItem('weKnowRecentSearches');
            localStorage.removeItem('weKnowAuthToken');
          } else {
            // Token is invalid, clear storage
            userDataService.clearUserData();
            setIsAuthenticated(false);
          }
        } catch (err) {
          console.error('Auth check error:', err);
          // Token is invalid, clear storage
          userDataService.clearUserData();
          setIsAuthenticated(false);
        }
      }
    };
    
    checkAuth();
  }, []);

  const handleReplaceIngredients = (updatedIngredients) => {
    setIngredients(updatedIngredients);
  };

  const handleLogout = async () => {
    try {
      const token = localStorage.getItem('weKnowToken');
      if (token) {
        // Call logout endpoint
        await axios.post('http://localhost:8000/auth/logout', {}, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
      }
    } catch (err) {
      console.error('Logout error:', err);
      // Continue with logout even if API call fails
    } finally {
      // Clear authentication but keep data in database
      userDataService.clearUserData();
      setIsAuthenticated(false);
      setShowLoginForm(false);
      setShowSignupScreen(false);
      setIngredients([]);
      setRecipeInfo(null);
      // Recent searches and orders will be cleared by useEffect when isAuthenticated becomes false
    }
  };

  const handleSubmit = async (e, overrideDishName = null) => {
    e.preventDefault();
    
    const dishToUse = overrideDishName || dishName;
    
    if (!dishToUse.trim()) {
      setError('Please enter a dish name');
      return;
    }

    setLoading(true);
    setError('');
    setIngredients([]);
    setRecipeInfo(null);
    setNutritionInfo(null);
    setAllergyWarning(null);
    setAlternativeSuggestions(null);

    try {
      const token = localStorage.getItem('weKnowToken');
      const headers = {
        'Content-Type': 'application/json'
      };
      
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await axios.post('http://localhost:8000/ingredients', {
        dish_name: dishToUse.trim(),
        servings: servings,
        include_nutrition: true
      }, { headers });

      console.log('Response received:', response.data);

      if (response.data.success) {
        console.log('Setting ingredients:', response.data.ingredients);
        console.log('Setting recipe info:', response.data.recipe_info);
        console.log('Setting allergy warning:', response.data.allergy_warning);
        console.log('Setting alternative suggestions:', response.data.alternative_suggestions);
        setIngredients(response.data.ingredients);
        setRecipeInfo(response.data.recipe_info);
        setNutritionInfo(response.data.nutrition || null);
        setAllergyWarning(response.data.allergy_warning || null);
        setAlternativeSuggestions(response.data.alternative_suggestions || null);
        
        // Add to recent searches in database
        if (isAuthenticated) {
          try {
            await userDataService.addRecentSearch(dishToUse.trim());
            // Update local state
            setRecentSearches(prev => {
              const filtered = prev.filter(item => item !== dishToUse.trim());
              return [dishToUse.trim(), ...filtered].slice(0, 4); // Keep only 4 recent searches
            });
          } catch (error) {
            console.error('Error saving recent search:', error);
          }
        } else {
          // For non-authenticated users, just update local state
          setRecentSearches(prev => {
            const filtered = prev.filter(item => item !== dishToUse.trim());
            return [dishToUse.trim(), ...filtered].slice(0, 4);
          });
        }
      } else {
        setError(response.data.error || 'Failed to fetch ingredients');
      }
    } catch (err) {
      console.error('Error fetching ingredients:', err);
      if (err.response?.data?.error) {
        setError(err.response.data.error);
      } else if (err.response?.status === 404) {
        setError(`No recipe found for "${dishToUse}". Try a different dish name.`);
      } else {
        setError('Failed to connect to the server. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };



  const handleRecentSearchClick = async (dish) => {
    setDishName(dish);
    
    // Add to recent searches in database
    if (isAuthenticated) {
      try {
        await userDataService.addRecentSearch(dish);
        // Update local state to reflect the new search
        setRecentSearches(prev => {
          const filtered = prev.filter(item => item !== dish);
          return [dish, ...filtered].slice(0, 4);
        });
      } catch (error) {
        console.error('Error adding recent search:', error);
      }
    }
  };

  const addOrder = async (order) => {
    if (isAuthenticated) {
      try {
        // Save to database
        const token = localStorage.getItem('weKnowToken');
        const response = await axios.post('http://localhost:8000/user/orders', {
          dish_name: order.dish_name,
          ingredients: order.ingredients,
          servings: order.servings
        }, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.data.success) {
          console.log('Order saved to database successfully:', response.data);
          // Don't update local state - let the components fetch from database
          refreshOrders(); // Refresh orders after successful order placement
        } else {
          console.error('Failed to save order to database:', response.data.error);
        }
      } catch (error) {
        console.error('Error saving order to database:', error);
      }
    }

    // Show success message and refresh the search page after order is placed
    setError(''); // Clear any existing errors
    setTimeout(() => {
      // Show a brief success message
      setSuccessMessage('✅ Order placed successfully! Refreshing search page...');
      
      setTimeout(() => {
        // Clear everything and refresh the search page
        setDishName('');
        setIngredients([]);
        setRecipeInfo(null);
        setError('');
        setSuccessMessage('');
        setLoading(false);
      }, 1500); // Show success message for 1.5 seconds
    }, 500); // Small delay to show order success
  };

  const deleteIngredient = (index) => {
    setIngredients(prevIngredients => {
      const newIngredients = [...prevIngredients];
      newIngredients.splice(index, 1);
      return newIngredients;
    });
  };


  const dishInputRef = useRef(null);

  useEffect(() => {
    if (dishInputRef.current) {
      dishInputRef.current.focus();
    }
  }, [dishName]);

  return (
    <Router>
      <div className="App">

        {isAuthenticated ? (
          <AppLayout 
            user={JSON.parse(localStorage.getItem('weKnowUser') || '{}')}
            handleLogout={handleLogout}
          >
            <Routes>
              <Route path="/" element={
                <HomePage 
                  dish={dishName}
                  setDish={setDishName}
                  ingredients={ingredients}
                  loading={loading}
                  setLoading={setLoading}
                  error={error}
                  setError={setError}
                  successMessage={successMessage}
                  setSuccessMessage={setSuccessMessage}
                  handleSubmit={handleSubmit}
                  onReplaceIngredients={handleReplaceIngredients}
                  handleRecentSearchClick={handleRecentSearchClick}
                  recentSearches={recentSearches}
                  recipeInfo={recipeInfo}
                  nutritionInfo={nutritionInfo}
                  allergyWarning={allergyWarning}
                  alternativeSuggestions={alternativeSuggestions}
                  servings={servings}
                  setServings={setServings}
                  orders={orders}
                  addOrder={addOrder}
                  deleteIngredient={deleteIngredient}
                />
              } />
              <Route path="/order-history" element={<OrderHistory />} />
              <Route path="/saved-addresses" element={<SavedAddresses />} />
              <Route path="/track-orders" element={<TrackOrders />} />
              <Route path="/settings" element={<Settings />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </AppLayout>
        ) : showSignupScreen ? (
          <SignupModal
            isOpen={showSignupScreen}
            onClose={() => setShowSignupScreen(false)}
            onSignup={(userData) => {
              setIsAuthenticated(true);
              setShowSignupScreen(false);
              // Data will be loaded from database via useEffect
            }}
          />
        ) : (
          <LandingPage 
            onLoginClick={() => setShowLoginForm(true)}
            onSignupClick={() => setShowSignupScreen(true)}
            navigateToHome={navigateToHome}
          />
        )}

        {/* Login Form Modal */}
        {showLoginForm && (
          <LoginModal
            isOpen={showLoginForm}
            onClose={() => setShowLoginForm(false)}
            onLogin={() => {
              console.log('onLogin callback called - setting isAuthenticated to true');
              setIsAuthenticated(true);
              setShowLoginForm(false); // Close the login modal
              // Data will be loaded from database via useEffect
            }}
          />
        )}


      </div>
    </Router>
  );
}

export default App; 