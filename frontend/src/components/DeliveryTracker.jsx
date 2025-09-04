import React, { useState, useEffect } from 'react';

const DeliveryTracker = ({ order, onClose }) => {
  const [deliveryStatus, setDeliveryStatus] = useState('preparing');
  const [estimatedTime, setEstimatedTime] = useState(30);
  const [currentLocation, setCurrentLocation] = useState({
    lat: 37.7749,
    lng: -122.4194
  });
  const [deliveryLocation] = useState({
    lat: 37.7849,
    lng: -122.4094
  });

  // Simulate delivery progress
  useEffect(() => {
    const statuses = ['preparing', 'on_the_way', 'nearby', 'delivered'];
    let currentIndex = 0;

    const interval = setInterval(() => {
      if (currentIndex < statuses.length - 1) {
        currentIndex++;
        setDeliveryStatus(statuses[currentIndex]);
        
        // Update estimated time
        setEstimatedTime(prev => Math.max(0, prev - 10));
        
        // Simulate movement on map
        if (statuses[currentIndex] === 'on_the_way') {
          setCurrentLocation(prev => ({
            lat: prev.lat + 0.001,
            lng: prev.lng + 0.001
          }));
        } else if (statuses[currentIndex] === 'nearby') {
          setCurrentLocation(deliveryLocation);
        }
      } else {
        clearInterval(interval);
      }
    }, 10000); // Update every 10 seconds

    return () => clearInterval(interval);
  }, [deliveryLocation]);

  const getStatusInfo = () => {
    switch (deliveryStatus) {
      case 'preparing':
        return {
          title: 'Preparing Your Order',
          description: 'Your delicious meal is being prepared with care',
          icon: '👨‍🍳',
          color: '#ffc107'
        };
      case 'on_the_way':
        return {
          title: 'On The Way',
          description: 'Your order is on its way to you',
          icon: '🚚',
          color: '#17a2b8'
        };
      case 'nearby':
        return {
          title: 'Almost There!',
          description: 'Your delivery is nearby',
          icon: '📍',
          color: '#28a745'
        };
      case 'delivered':
        return {
          title: 'Delivered!',
          description: 'Enjoy your meal!',
          icon: '✅',
          color: '#28a745'
        };
      default:
        return {
          title: 'Order Status',
          description: 'Tracking your order',
          icon: '📦',
          color: '#6c757d'
        };
    }
  };

  const statusInfo = getStatusInfo();

  return (
    <div className="delivery-tracker-modal">
      <div className="delivery-tracker-content">
        <button className="close-button" onClick={onClose}>×</button>
        
        <div className="delivery-header">
          <h2>Delivery Tracking</h2>
          <div className="order-info">
            <h3>{order.dish}</h3>
            <p>Order #{order.orderDate ? order.orderDate.slice(-8) : 'N/A'}</p>
          </div>
        </div>

        <div className="delivery-status">
          <div className="status-indicator" style={{ backgroundColor: statusInfo.color }}>
            <span className="status-icon">{statusInfo.icon}</span>
            <div className="status-text">
              <h4>{statusInfo.title}</h4>
              <p>{statusInfo.description}</p>
            </div>
          </div>
          
          {deliveryStatus !== 'delivered' && (
            <div className="estimated-time">
              <span className="time-icon">⏱️</span>
              <span>Estimated delivery: {estimatedTime} minutes</span>
            </div>
          )}
        </div>

        <div className="map-container">
          <div className="map-placeholder">
            <div className="map-content">
              <div className="map-title">📍 Live Delivery Map</div>
              <div className="map-coordinates">
                <div className="location-info">
                  <div className="location restaurant">
                    <span className="location-icon">🏪</span>
                    <span>Restaurant</span>
                  </div>
                  <div className="location delivery">
                    <span className="location-icon">🏠</span>
                    <span>Your Address</span>
                  </div>
                  {deliveryStatus !== 'preparing' && (
                    <div className="location driver" style={{
                      left: `${((currentLocation.lat - 37.7749) / 0.01) * 100}%`,
                      top: `${((currentLocation.lng - (-122.4194)) / 0.01) * 100}%`
                    }}>
                      <span className="location-icon">🚚</span>
                      <span>Driver</span>
                    </div>
                  )}
                </div>
                <div className="route-line"></div>
              </div>
              <div className="map-note">
                              <p>📍 {order.address || 'N/A'}</p>
              <p>🕐 Order placed: {order.orderDate ? new Date(order.orderDate).toLocaleTimeString() : 'N/A'}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="delivery-details">
          <h4>Delivery Details</h4>
          <div className="details-grid">
            <div className="detail-item">
              <span className="detail-label">Order:</span>
              <span className="detail-value">{order.dish || 'N/A'}</span>
            </div>
            <div className="detail-item">
              <span className="detail-label">Quantity:</span>
              <span className="detail-value">{order.quantity || 'N/A'}</span>
            </div>
            <div className="detail-item">
              <span className="detail-label">Total:</span>
              <span className="detail-value">${order.totalPrice || 'N/A'}</span>
            </div>
            <div className="detail-item">
              <span className="detail-label">Payment:</span>
              <span className="detail-value">{order.paymentMethod || 'N/A'}</span>
            </div>
            <div className="detail-item full-width">
              <span className="detail-label">Address:</span>
              <span className="detail-value">{order.address || 'N/A'}</span>
            </div>
          </div>
        </div>

        {deliveryStatus === 'delivered' && (
          <div className="delivery-complete">
            <div className="complete-icon">🎉</div>
            <h3>Order Delivered Successfully!</h3>
            <p>Thank you for choosing We Know. Enjoy your meal!</p>
            <button className="rate-order-button" onClick={onClose}>
              Rate Your Experience
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default DeliveryTracker; 