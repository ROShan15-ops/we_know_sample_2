import React, { useState, useEffect } from 'react';
import axios from 'axios';

const DeliveryDashboard = ({ onClose, selectedDish, selectedServings, addOrder }) => {
  const [shops, setShops] = useState([]);
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedShop, setSelectedShop] = useState(null);
  const [deliveryOrder, setDeliveryOrder] = useState(null);
  const [creatingOrder, setCreatingOrder] = useState(false);
  const [showCheckout, setShowCheckout] = useState(false);
  const [orderAdded, setOrderAdded] = useState(false);
  const [checkoutData, setCheckoutData] = useState({
    fullName: '',
    phone: '',
    address: '',
    city: '',
    zipCode: '',
    paymentMethod: 'credit_card',
    cardNumber: '',
    expiryDate: '',
    cvv: ''
  });

  // Fetch shops and agents on component mount
  useEffect(() => {
    fetchShopsAndAgents();
  }, []);

  // Add order to the orders list when successfully created
  useEffect(() => {
    if (deliveryOrder && deliveryOrder.success && addOrder && !orderAdded) {
      const orderToAdd = {
        dish_name: selectedDish,
        servings: selectedServings || 2,
        ingredients: deliveryOrder.ingredients || []
      };
      addOrder(orderToAdd);
      setOrderAdded(true);
      
      // Close the delivery dashboard after successful order placement
      setTimeout(() => {
        onClose();
      }, 1500); // Give user time to see the success message
    }
  }, [deliveryOrder, addOrder, selectedDish, selectedServings, orderAdded, onClose]);

  const fetchShopsAndAgents = async () => {
    try {
      setLoading(true);
      
      // Fetch shops
      const shopsResponse = await axios.get('http://localhost:8000/delivery/shops');
      setShops(shopsResponse.data.shops);
      
      // Fetch agents
      const agentsResponse = await axios.get('http://localhost:8000/delivery/agents');
      setAgents(agentsResponse.data.agents);
      
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch delivery data');
      setLoading(false);
      console.error('Error fetching delivery data:', err);
    }
  };

  const createDeliveryOrder = async () => {
    if (!selectedShop || !selectedDish) return;

    // Validate checkout form if showing checkout
    if (showCheckout) {
      const validationError = validateCheckoutForm();
      if (validationError) {
        setError(validationError);
        return;
      }
    }

    try {
      setCreatingOrder(true);
      setOrderAdded(false); // Reset the flag when creating a new order
      
      const orderData = {
        dish_name: selectedDish,
        servings: selectedServings || 2,
        user_location: {
          lat: 37.7749, // Default San Francisco location
          lng: -122.4194
        },
        checkout_data: showCheckout ? checkoutData : null
      };

      // Get authentication token
      const token = localStorage.getItem('weKnowToken');
      const headers = {
        'Content-Type': 'application/json'
      };
      
      // Add authorization header if token exists
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
      
      // Use the test endpoint that now supports authentication
      const response = await axios.post('http://localhost:8000/delivery/test', orderData, {
        headers: headers
      });

      console.log('Delivery order response:', response.data);
      setDeliveryOrder(response.data);
      setCreatingOrder(false);
    } catch (err) {
      console.error('Error creating delivery order:', err);
      console.error('Error response:', err.response?.data);
      
      // Handle different error types
      if (err.response?.status === 404) {
        setError('No ingredients found for this dish. Please try a different dish.');
      } else if (err.response?.status === 500) {
        setError('Server error. Please try again later.');
      } else if (err.response?.data?.error) {
        setError(err.response.data.error);
      } else {
        setError('Failed to create delivery order. Please try again.');
      }
      
      setCreatingOrder(false);
    }
  };

  const getShopCoverageColor = (coverage) => {
    if (coverage >= 80) return '#28a745'; // Green
    if (coverage >= 60) return '#ffc107'; // Yellow
    return '#dc3545'; // Red
  };

  const handleCheckoutChange = (field, value) => {
    setCheckoutData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const validateCheckoutForm = () => {
    const required = ['fullName', 'phone', 'address', 'city', 'zipCode'];
    for (const field of required) {
      if (!checkoutData[field].trim()) {
        return `Please fill in ${field.replace(/([A-Z])/g, ' $1').toLowerCase()}`;
      }
    }
    
    if (checkoutData.paymentMethod === 'credit_card') {
      if (!checkoutData.cardNumber || !checkoutData.expiryDate || !checkoutData.cvv) {
        return 'Please fill in all credit card details';
      }
    }
    
    return null;
  };

  if (loading) {
    return (
      <div className="delivery-dashboard-modal">
        <div className="delivery-dashboard-content">
          <div className="loading-spinner">
            <div className="spinner"></div>
            <p>Loading delivery options...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="delivery-dashboard-modal">
        <div className="delivery-dashboard-content">
          <button className="close-button" onClick={onClose}>×</button>
          <div className="error-message">
            <h3>⚠️ Error</h3>
            <p>{error}</p>
            <button onClick={fetchShopsAndAgents}>Retry</button>
          </div>
        </div>
      </div>
    );
  }

  if (deliveryOrder && deliveryOrder.success) {
    return (
      <div className="delivery-dashboard-modal">
        <div className="delivery-dashboard-content">
          <button className="close-button" onClick={onClose}>×</button>
          
          <div className="order-success">
            <div className="success-icon">🎉</div>
            <h2>Delivery Order Created!</h2>
            <p>Your ingredients are on the way!</p>
            
            <div className="order-details">
              <h3>Order Details</h3>
              <div className="order-info">
                <p><strong>Order ID:</strong> {deliveryOrder.order_id || 'N/A'}</p>
                <p><strong>Dish:</strong> {deliveryOrder.dish || 'N/A'}</p>
                <p><strong>Shop:</strong> {deliveryOrder.top_shop?.name || 'N/A'}</p>
                <p><strong>Distance:</strong> {deliveryOrder.top_shop?.distance_km || 'N/A'} km</p>
                <p><strong>Match Percentage:</strong> {deliveryOrder.top_shop?.match_percent || 'N/A'}%</p>
                <p><strong>Delivery Agent:</strong> {deliveryOrder.delivery_agent?.name || 'N/A'}</p>
                <p><strong>Estimated Time:</strong> {deliveryOrder.estimated_delivery_time_minutes || 'N/A'} minutes</p>
              </div>
              
              <div className="ingredient-coverage">
                <h4>Ingredient Coverage</h4>
                <p className="coverage-text">{deliveryOrder.top_shop?.match_percent || 0}% coverage</p>
                
                {deliveryOrder.top_shop?.available_ingredients && deliveryOrder.top_shop.available_ingredients.length > 0 && (
                  <div className="available-ingredients">
                    <h5>✅ Available Ingredients:</h5>
                    <ul>
                      {deliveryOrder.top_shop.available_ingredients.slice(0, 5).map((ingredient, index) => (
                        <li key={index}>
                          {ingredient.ingredient} ({ingredient.quantity} {ingredient.unit})
                        </li>
                      ))}
                      {deliveryOrder.top_shop.available_ingredients.length > 5 && (
                        <li>... and {deliveryOrder.top_shop.available_ingredients.length - 5} more</li>
                      )}
                    </ul>
                  </div>
                )}
                
                {deliveryOrder.top_shop?.missing_ingredients && deliveryOrder.top_shop.missing_ingredients.length > 0 && (
                  <div className="missing-ingredients">
                    <h5>❌ Missing Ingredients:</h5>
                    <ul>
                      {deliveryOrder.top_shop.missing_ingredients.slice(0, 3).map((ingredient, index) => (
                        <li key={index}>
                          {ingredient.ingredient} ({ingredient.quantity} {ingredient.unit})
                        </li>
                      ))}
                      {deliveryOrder.top_shop.missing_ingredients.length > 3 && (
                        <li>... and {deliveryOrder.top_shop.missing_ingredients.length - 3} more</li>
                      )}
                    </ul>
                  </div>
                )}
              </div>
            </div>
            
            <button className="track-order-button" onClick={onClose}>
              Track Order
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="delivery-dashboard-modal">
      <div className="delivery-dashboard-content">
        <button className="close-button" onClick={onClose}>×</button>
        
        <div className="delivery-header">
          <h2>🚚 WeKno Delivery</h2>
          <p>Get ingredients delivered to your door!</p>
        </div>

        {selectedDish && (
          <div className="selected-dish-info">
            <h3>🍽️ {selectedDish}</h3>
            <p>Servings: {selectedServings || 2}</p>
          </div>
        )}

        <div className="shops-section">
          <h3>🏪 Available Shops</h3>
          <div className="shops-grid">
            {shops.map((shop, index) => (
              <div 
                key={index} 
                className={`shop-card ${selectedShop?.name === shop.name ? 'selected' : ''}`}
                onClick={() => setSelectedShop(shop)}
              >
                <div className="shop-header">
                  <h4>{shop.name}</h4>
                  <span className="inventory-count">{shop.inventory_count} items</span>
                </div>
                <div className="shop-location">
                  <span>📍 {shop.location.lat.toFixed(4)}, {shop.location.lng.toFixed(4)}</span>
                </div>
                <div className="shop-inventory">
                  <p>Sample items:</p>
                  <div className="inventory-tags">
                    {shop.inventory.slice(0, 6).map((item, idx) => (
                      <span key={idx} className="inventory-tag">{item}</span>
                    ))}
                    {shop.inventory.length > 6 && (
                      <span className="inventory-tag">+{shop.inventory.length - 6} more</span>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="agents-section">
          <h3>🚚 Delivery Agents</h3>
          <div className="agents-grid">
            {agents.map((agent, index) => (
              <div key={index} className="agent-card">
                <div className="agent-status" style={{ 
                  backgroundColor: agent.status === 'available' ? '#28a745' : '#dc3545' 
                }}>
                  {agent.status === 'available' ? '🟢' : '🔴'}
                </div>
                <div className="agent-info">
                  <h4>{agent.name}</h4>
                  <p>Status: {agent.status}</p>
                  <p>📍 {agent.current_location.lat.toFixed(4)}, {agent.current_location.lng.toFixed(4)}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {selectedShop && !showCheckout && (
          <div className="delivery-actions">
            <div className="selected-shop-info">
              <h4>Selected Shop: {selectedShop.name}</h4>
              <p>Ready to create delivery order</p>
            </div>
            <button 
              className="create-order-button"
              onClick={() => setShowCheckout(true)}
              disabled={creatingOrder}
            >
              💳 Proceed to Checkout
            </button>
          </div>
        )}

        {selectedShop && showCheckout && (
          <div className="checkout-section">
            <div className="checkout-header">
              <h3>💳 Checkout</h3>
              <button 
                className="back-button"
                onClick={() => setShowCheckout(false)}
              >
                ← Back to Shop Selection
              </button>
            </div>

            <div className="checkout-form">
              <div className="form-section">
                <h4>📋 Delivery Information</h4>
                <div className="form-row">
                  <div className="form-group">
                    <label>Full Name *</label>
                    <input
                      type="text"
                      value={checkoutData.fullName}
                      onChange={(e) => handleCheckoutChange('fullName', e.target.value)}
                      placeholder="John Doe"
                    />
                  </div>
                  <div className="form-group">
                    <label>Phone Number *</label>
                    <input
                      type="tel"
                      value={checkoutData.phone}
                      onChange={(e) => handleCheckoutChange('phone', e.target.value)}
                      placeholder="+1 (555) 123-4567"
                    />
                  </div>
                </div>
                <div className="form-group">
                  <label>Street Address *</label>
                  <input
                    type="text"
                    value={checkoutData.address}
                    onChange={(e) => handleCheckoutChange('address', e.target.value)}
                    placeholder="123 Main Street"
                  />
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label>City *</label>
                    <input
                      type="text"
                      value={checkoutData.city}
                      onChange={(e) => handleCheckoutChange('city', e.target.value)}
                      placeholder="San Francisco"
                    />
                  </div>
                  <div className="form-group">
                    <label>ZIP Code *</label>
                    <input
                      type="text"
                      value={checkoutData.zipCode}
                      onChange={(e) => handleCheckoutChange('zipCode', e.target.value)}
                      placeholder="94102"
                    />
                  </div>
                </div>
              </div>

              <div className="form-section">
                <h4>💳 Payment Method</h4>
                <div className="payment-methods">
                  <label className="payment-option">
                    <input
                      type="radio"
                      name="paymentMethod"
                      value="credit_card"
                      checked={checkoutData.paymentMethod === 'credit_card'}
                      onChange={(e) => handleCheckoutChange('paymentMethod', e.target.value)}
                    />
                    <span>Credit Card</span>
                  </label>
                  <label className="payment-option">
                    <input
                      type="radio"
                      name="paymentMethod"
                      value="cash"
                      checked={checkoutData.paymentMethod === 'cash'}
                      onChange={(e) => handleCheckoutChange('paymentMethod', e.target.value)}
                    />
                    <span>Cash on Delivery</span>
                  </label>
                </div>

                {checkoutData.paymentMethod === 'credit_card' && (
                  <div className="credit-card-details">
                    <div className="form-group">
                      <label>Card Number *</label>
                      <input
                        type="text"
                        value={checkoutData.cardNumber}
                        onChange={(e) => handleCheckoutChange('cardNumber', e.target.value)}
                        placeholder="1234 5678 9012 3456"
                        maxLength="19"
                      />
                    </div>
                    <div className="form-row">
                      <div className="form-group">
                        <label>Expiry Date *</label>
                        <input
                          type="text"
                          value={checkoutData.expiryDate}
                          onChange={(e) => handleCheckoutChange('expiryDate', e.target.value)}
                          placeholder="MM/YY"
                          maxLength="5"
                        />
                      </div>
                      <div className="form-group">
                        <label>CVV *</label>
                        <input
                          type="text"
                          value={checkoutData.cvv}
                          onChange={(e) => handleCheckoutChange('cvv', e.target.value)}
                          placeholder="123"
                          maxLength="4"
                        />
                      </div>
                    </div>
                  </div>
                )}
              </div>

              <div className="order-summary">
                <h4>📋 Order Summary</h4>
                <div className="summary-item">
                  <span>Dish:</span>
                  <span>{selectedDish}</span>
                </div>
                <div className="summary-item">
                  <span>Servings:</span>
                  <span>{selectedServings || 2}</span>
                </div>
                <div className="summary-item">
                  <span>Shop:</span>
                  <span>{selectedShop.name}</span>
                </div>
                <div className="summary-item total">
                  <span>Estimated Total:</span>
                  <span>$25.99</span>
                </div>
              </div>

              <button 
                className="create-order-button"
                onClick={createDeliveryOrder}
                disabled={creatingOrder}
              >
                {creatingOrder ? 'Creating Order...' : '🚚 Place Order'}
              </button>
            </div>
          </div>
        )}

        <div className="delivery-note">
          <p>💡 <strong>How it works:</strong></p>
          <ul>
            <li>We fetch real ingredients from TheMealDB</li>
            <li>Match ingredients with nearby shop inventory</li>
            <li>Find the best shop with highest ingredient coverage</li>
            <li>Assign nearest available delivery agent</li>
            <li>Calculate realistic delivery time</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default DeliveryDashboard; 