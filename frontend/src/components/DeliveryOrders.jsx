import React, { useState, useEffect } from 'react';
import axios from 'axios';

const DeliveryOrders = ({ onClose }) => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Mock orders for demonstration (in real app, these would come from backend)
  const mockOrders = [
    {
      order_id: "WK81260",
      dish: "Pizza",
      created_at: "2025-07-21T01:49:14",
      shop: {
        name: "Super Foods",
        distance_km: 2.1,
        distance_text: "2.1 km",
        duration_text: "8 mins"
      },
      assigned_delivery_agent: {
        name: "John Smith",
        status: "On the way"
      },
      estimated_delivery_time: "25-35 minutes",
      order_details: {
        servings: 2,
        total_ingredients: 11,
        available_ingredients_count: 10,
        missing_ingredients_count: 1
      },
      status: "in_progress"
    },
    {
      order_id: "WK75569",
      dish: "Carbonara",
      created_at: "2025-07-21T01:49:39",
      shop: {
        name: "Fresh Mart",
        distance_km: 1.8,
        distance_text: "1.8 km",
        duration_text: "6 mins"
      },
      assigned_delivery_agent: {
        name: "Sarah Johnson",
        status: "Picking up"
      },
      estimated_delivery_time: "20-30 minutes",
      order_details: {
        servings: 2,
        total_ingredients: 6,
        available_ingredients_count: 2,
        missing_ingredients_count: 4
      },
      status: "preparing"
    },
    {
      order_id: "WK64216",
      dish: "Chicken Curry",
      created_at: "2025-07-21T01:53:47",
      shop: {
        name: "Local Grocery",
        distance_km: 3.2,
        distance_text: "3.2 km",
        duration_text: "12 mins"
      },
      assigned_delivery_agent: {
        name: "Mike Wilson",
        status: "Delivered"
      },
      estimated_delivery_time: "35-45 minutes",
      order_details: {
        servings: 3,
        total_ingredients: 16,
        available_ingredients_count: 10,
        missing_ingredients_count: 6
      },
      status: "delivered"
    }
  ];

  useEffect(() => {
    // In a real app, you would fetch orders from the backend
    // For now, we'll use mock data
    setTimeout(() => {
      setOrders(mockOrders);
      setLoading(false);
    }, 1000);
  }, []);

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'preparing':
        return '#f39c12';
      case 'in_progress':
        return '#3498db';
      case 'delivered':
        return '#27ae60';
      default:
        return '#95a5a6';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'preparing':
        return 'Preparing';
      case 'in_progress':
        return 'On the way';
      case 'delivered':
        return 'Delivered';
      default:
        return 'Unknown';
    }
  };

  if (loading) {
    return (
      <div className="orders-modal">
        <div className="orders-content">
          <button className="close-button" onClick={onClose}>×</button>
          <div className="loading">
            <div className="spinner"></div>
            <p>Loading your orders...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="orders-modal">
      <div className="orders-content">
        <button className="close-button" onClick={onClose}>×</button>
        
        <div className="orders-header">
          <h2>🚚 My Delivery Orders</h2>
          <p>Track your ingredient delivery orders</p>
        </div>
        
        {orders.length === 0 ? (
          <div className="no-orders">
            <div className="no-orders-icon">📋</div>
            <h3>No Delivery Orders Yet</h3>
            <p>Start exploring dishes and get ingredients delivered!</p>
          </div>
        ) : (
          <div className="orders-list">
            {orders.map((order, index) => (
              <div key={index} className="order-card delivery-order-card">
                <div className="order-header">
                  <div className="order-title">
                    <h3 className="order-dish-name">{order.dish}</h3>
                    <span className="order-id">#{order.order_id}</span>
                  </div>
                  <div className="order-status-badge" style={{ backgroundColor: getStatusColor(order.status) }}>
                    {getStatusText(order.status)}
                  </div>
                </div>
                
                <div className="order-details">
                  <div className="order-info">
                    <p><strong>🛒 Shop:</strong> {order.shop.name}</p>
                    <p><strong>📦 Servings:</strong> {order.order_details.servings}</p>
                    <p><strong>📅 Ordered:</strong> {formatDate(order.created_at)}</p>
                    <p><strong>⏱️ Delivery Time:</strong> {order.estimated_delivery_time}</p>
                  </div>
                  
                  <div className="delivery-info">
                    <p><strong>🚚 Delivery Agent:</strong> {order.assigned_delivery_agent.name}</p>
                    <p><strong>📍 Distance:</strong> {order.shop.distance_text} ({order.shop.duration_text})</p>
                    <p><strong>📊 Ingredient Coverage:</strong> {order.order_details.available_ingredients_count}/{order.order_details.total_ingredients} available</p>
                  </div>
                </div>
                
                <div className="order-progress">
                  <div className="progress-bar">
                    <div 
                      className="progress-fill" 
                      style={{ 
                        width: `${(order.order_details.available_ingredients_count / order.order_details.total_ingredients) * 100}%`,
                        backgroundColor: order.order_details.available_ingredients_count / order.order_details.total_ingredients > 0.7 ? '#27ae60' : '#f39c12'
                      }}
                    ></div>
                  </div>
                  <p className="progress-text">
                    {order.order_details.available_ingredients_count} of {order.order_details.total_ingredients} ingredients available
                  </p>
                </div>

                <div className="order-actions">
                  <button className="track-delivery-button">
                    🗺️ Track Delivery
                  </button>
                  <button className="view-details-button">
                    📋 View Details
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default DeliveryOrders; 