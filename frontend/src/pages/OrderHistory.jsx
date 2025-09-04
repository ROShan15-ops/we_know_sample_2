import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './Pages.css';

const OrderHistory = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchOrders = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const token = localStorage.getItem('weKnowToken');
      
      if (!token) {
        setError('Please login to view your orders');
        setLoading(false);
        return;
      }

      const response = await axios.get('http://localhost:8000/user/orders', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.data.success) {
        setOrders(response.data.orders || []);
      } else {
        setError(response.data.error || 'Failed to load orders');
      }
    } catch (err) {
      if (err.response?.status === 401) {
        setError('Please login to view your orders');
      } else {
        setError(`Failed to load orders: ${err.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  const handleRefresh = () => {
    fetchOrders();
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <Link to="/" className="back-button">
          ← Back to Home
        </Link>
        <h1>Order History</h1>
        <div>
          <button onClick={handleRefresh} className="refresh-button">
            🔄 Refresh
          </button>
        </div>
      </div>

      <div className="page-content">
        {loading ? (
          <div className="loading-state">
            <div className="loading-spinner"></div>
            <p>Loading your orders...</p>
          </div>
        ) : error ? (
          <div className="error-state">
            <div className="error-icon">⚠️</div>
            <h3>Error Loading Orders</h3>
            <p>{error}</p>
            <button onClick={handleRefresh} className="retry-button">
              Try Again
            </button>
          </div>
        ) : orders.length > 0 ? (
          <div className="orders-list">
            <h3>✅ Found {orders.length} orders:</h3>
            {orders.map((order) => (
              <div key={order.id} className="order-card">
                <div className="order-header">
                  <h3>{order.dish_name}</h3>
                  <span className={`status-badge ${(order.status || 'pending').toLowerCase()}`}>
                    {order.status || 'Pending'}
                  </span>
                </div>
                
                <div className="order-details">
                  <p><strong>Order ID:</strong> {order.id || 'N/A'}</p>
                  <p><strong>Date:</strong> {order.timestamp ? new Date(order.timestamp).toLocaleDateString() : 'N/A'}</p>
                  <p><strong>Servings:</strong> {order.servings || 2}</p>
                </div>

                <div className="ingredients-section">
                  <h4>Ingredients Delivered:</h4>
                  <div className="ingredients-tags">
                    {order.ingredients && order.ingredients.length > 0 ? (
                      order.ingredients.map((ingredient, index) => {
                        const quantity = ingredient.quantity;
                        const unit = ingredient.unit || '';
                        const name = ingredient.ingredient || ingredient.name || 'Unknown ingredient';
                        
                        return (
                          <span key={index} className="ingredient-tag">
                            {quantity !== null ? `${quantity} ${unit} ` : ''}{name}
                          </span>
                        );
                      })
                    ) : (
                      <span className="ingredient-tag">No ingredients available</span>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-icon">📋</div>
            <h3>No Orders Found</h3>
            <p>You haven't placed any orders yet.</p>
            <Link to="/" className="cta-button">
              Place Your First Order
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};

export default OrderHistory; 