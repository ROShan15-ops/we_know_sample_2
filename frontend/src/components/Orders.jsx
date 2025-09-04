import React, { useState, useCallback, useMemo, useEffect } from 'react';
import DeliveryTracker from './DeliveryTracker.jsx';

const Orders = ({ orders, onClose }) => {
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [showTracker, setShowTracker] = useState(false);
  const [orderStatuses, setOrderStatuses] = useState({});
  const [countdownTimers, setCountdownTimers] = useState({});
  
  // Memoize orders to prevent unnecessary re-renders
  const memoizedOrders = useMemo(() => orders || [], [orders]);
  
  const formatDate = useCallback((dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }, []);

  // Timer to automatically update order status
  useEffect(() => {
    const timers = {};
    const countdownIntervals = {};
    
    memoizedOrders.forEach((order, index) => {
      if (!orderStatuses[index]) {
        // Initialize status for new orders
        setOrderStatuses(prev => ({
          ...prev,
          [index]: 'pending'
        }));
        
        // Initialize countdown timer (30 seconds)
        setCountdownTimers(prev => ({
          ...prev,
          [index]: 30
        }));
        
        // Start countdown timer
        countdownIntervals[index] = setInterval(() => {
          setCountdownTimers(prev => {
            const newTime = prev[index] - 1;
            if (newTime <= 0) {
              clearInterval(countdownIntervals[index]);
              return { ...prev, [index]: 0 };
            }
            return { ...prev, [index]: newTime };
          });
        }, 1000);
        
        // Set timer to change status from pending to completed after 30 seconds
        timers[index] = setTimeout(() => {
          setOrderStatuses(prev => ({
            ...prev,
            [index]: 'completed'
          }));
        }, 30000); // 30 seconds
      }
    });

    // Cleanup timers on unmount
    return () => {
      Object.values(timers).forEach(timer => clearTimeout(timer));
      Object.values(countdownIntervals).forEach(interval => clearInterval(interval));
    };
  }, [memoizedOrders, orderStatuses]);

  const getStatusDisplay = (index) => {
    const status = orderStatuses[index] || 'pending';
    switch (status) {
      case 'pending':
        return { text: 'Pending', color: '#ffc107', icon: '⏳' };
      case 'completed':
        return { text: 'Completed', color: '#28a745', icon: '✅' };
      default:
        return { text: 'Pending', color: '#ffc107', icon: '⏳' };
    }
  };

  return (
    <div className="orders-modal">
      <div className="orders-content">
        <button className="close-button" onClick={onClose}>×</button>
        
        <div className="orders-header">
          <h2>My Orders</h2>
          <p>Track your order history and delivery status</p>

        </div>
        
        {memoizedOrders.length === 0 ? (
          <div className="no-orders">
            <div className="no-orders-icon">📋</div>
            <h3>No Orders Yet</h3>
            <p>Start exploring dishes and place your first order!</p>
          </div>
        ) : (
          <div className="orders-list">
            {memoizedOrders.map((order, index) => {
              const statusDisplay = getStatusDisplay(index);
              return (
                <div key={index} className="order-card">
                  <div className="order-header">
                    <h3 className="order-dish-name">{order.dish}</h3>
                                      <div className="order-actions">
                    <button 
                      className="track-delivery-button"
                      onClick={() => {
                        setSelectedOrder(order);
                        setShowTracker(true);
                      }}
                    >
                      🗺️ Track Delivery
                    </button>
                    <div className="status-container">
                      <span 
                        className="order-status" 
                        style={{ 
                          color: statusDisplay.color,
                          backgroundColor: statusDisplay.color + '20',
                          padding: '4px 8px',
                          borderRadius: '4px',
                          fontSize: '12px',
                          fontWeight: '500'
                        }}
                      >
                        {statusDisplay.icon} {statusDisplay.text}
                      </span>
                      {orderStatuses[index] === 'pending' && countdownTimers[index] > 0 && (
                        <span className="countdown-timer" style={{
                          fontSize: '10px',
                          color: '#666',
                          marginTop: '2px'
                        }}>
                          ⏱️ {countdownTimers[index]}s
                        </span>
                      )}
                    </div>
                  </div>
                  </div>
                
                <div className="order-details">
                  <div className="order-info">
                    <p><strong>Quantity:</strong> {order.quantity || 'N/A'}</p>
                    <p><strong>Total:</strong> ${order.totalPrice || 'N/A'}</p>
                    <p><strong>Payment:</strong> {order.paymentMethod || 'N/A'}</p>
                    <p><strong>Ordered:</strong> {order.orderDate ? formatDate(order.orderDate) : 'N/A'}</p>
                  </div>
                  
                  <div className="order-address">
                    <p><strong>Delivery Address:</strong></p>
                    <p>{order.address || 'N/A'}</p>
                  </div>
                </div>
                
                <div className="order-ingredients">
                  <h4>Ingredients:</h4>
                  <ul>
                    {order.ingredients && order.ingredients.length > 0 ? (
                      order.ingredients.map((ingredient, idx) => {
                        const quantity = ingredient.quantity;
                        const unit = ingredient.unit || '';
                        const name = ingredient.ingredient || 'Unknown ingredient';
                        
                        return (
                          <li key={idx}>
                            {quantity !== null ? `${quantity} ${unit} ` : ''}{name}
                          </li>
                        );
                      })
                    ) : (
                      <li>No ingredients available</li>
                    )}
                  </ul>
                </div>
              </div>
            );
            })}
          </div>
        )}

        {/* Delivery Tracker Modal */}
        {showTracker && selectedOrder && (
          <DeliveryTracker
            order={selectedOrder}
            onClose={() => {
              setShowTracker(false);
              setSelectedOrder(null);
            }}
          />
        )}
      </div>
    </div>
  );
};

export default Orders; 