import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './Pages.css';

const TrackOrders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchOrders = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const token = localStorage.getItem('weKnowToken');
      console.log('Token found:', !!token);
      
      if (!token) {
        setError('Please login to view your orders');
        setLoading(false);
        return;
      }

      console.log('Fetching orders from API...');
      const response = await axios.get('http://localhost:8000/user/orders', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      console.log('API Response:', response.data);
      
      if (response.data.success) {
        console.log('Orders fetched successfully:', response.data.orders);
        // Filter for active orders (pending or in_transit)
        const activeOrders = response.data.orders
          .filter(order => (order.status || 'pending') === 'pending' || (order.status || 'pending') === 'in_transit')
          .slice(0, 3); // Show only the 3 most recent orders as "active"
        
        setOrders(activeOrders || []);
      } else {
        console.error('Failed to load orders:', response.data.error);
        setError(response.data.error || 'Failed to load orders');
      }
    } catch (err) {
      console.error('Error fetching orders:', err);
      console.error('Error response:', err.response?.data);
      if (err.response?.status === 401) {
        setError('Please login to view your orders');
      } else {
        setError('Failed to load orders. Please try again.');
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
        <h1>Track Orders</h1>
        <button onClick={handleRefresh} className="refresh-button">
          🔄 Refresh
        </button>
      </div>

      <div className="page-content">
        {loading ? (
          <div className="loading-state">
            <div className="loading-spinner"></div>
            <p>Loading your active orders...</p>
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
            {orders.map((order) => (
              <div key={order.id} className="order-card">
                <div className="order-header">
                  <h3>{order.dish_name}</h3>
                  <span className={`status-badge ${(order.status || 'pending').toLowerCase().replace(' ', '-')}`}>
                    {order.status || 'Pending'}
                  </span>
                </div>
                
                <div className="order-details">
                  <p><strong>Order ID:</strong> {order.id || 'N/A'}</p>
                  <p><strong>Date:</strong> {order.timestamp ? new Date(order.timestamp).toLocaleDateString() : 'N/A'}</p>
                  <p><strong>Servings:</strong> {order.servings || 2}</p>
                  <p><strong>Status:</strong> {order.status || 'Pending'}</p>
                  {order.estimatedDelivery && (
                    <p><strong>Estimated Delivery:</strong> {order.estimatedDelivery}</p>
                  )}
                  {order.driver && (
                    <p><strong>Driver:</strong> {order.driver}</p>
                  )}
                  {order.location && (
                    <p><strong>Location:</strong> {order.location}</p>
                  )}
                </div>

                <div className="order-actions">
                  <button className="action-button">Track on Map</button>
                  <button className="action-button secondary">Contact Driver</button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-icon">🚚</div>
            <h3>No Active Orders</h3>
            <p>Your current deliveries will appear here</p>
            <Link to="/" className="cta-button">
              Order Something
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};

export default TrackOrders; 