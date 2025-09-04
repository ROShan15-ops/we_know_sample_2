import React, { useState, useEffect, useRef } from 'react';
import './MapAddressSelector.css';

const MapAddressSelector = ({ onAddressSelect, onClose }) => {
  const [map, setMap] = useState(null);
  const [marker, setMarker] = useState(null);
  const [selectedAddress, setSelectedAddress] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const mapRef = useRef(null);

  useEffect(() => {
    // Load Google Maps API
    const loadGoogleMaps = () => {
      if (window.google && window.google.maps) {
        initializeMap();
        return;
      }

      // For demo purposes, we'll use a mock map interface
      // In production, you would need a valid Google Maps API key with billing enabled
      console.log('🗺️ Loading mock Google Maps implementation for demo');
      setIsLoading(false);
      
      // Mock implementation for demo
      setTimeout(() => {
        setMap({ mock: true });
        setMarker({ mock: true });
        setIsLoading(false);
      }, 1000);
    };

    loadGoogleMaps();
  }, []);

  const initializeMap = () => {
    if (!mapRef.current) return;

    console.log('🗺️ Initializing mock Google Maps for demo');

    // Mock map for demo purposes
    const mockMap = {
      addListener: (event, callback) => {
        if (event === 'click') {
          // Mock click handler
          setTimeout(() => {
            const mockPosition = { lat: () => 40.7128, lng: () => -74.0060 };
            callback({ latLng: mockPosition });
          }, 500);
        }
      }
    };

    const mockMarker = {
      setPosition: (position) => {
        console.log('📍 Mock marker moved to:', position);
        reverseGeocode(position);
      }
    };

    setMap(mockMap);
    setMarker(mockMarker);
    setIsLoading(false);
  };

  const reverseGeocode = (position) => {
    console.log('🗺️ Mock reverse geocoding for position:', position.lat ? position.lat() : position.lat, position.lng ? position.lng() : position.lng);
    
    // Mock geocoding for demo purposes
    // In production, this would use Google's Geocoding API
    setTimeout(() => {
      const mockAddress = {
        fullAddress: '123 Main Street, New York, NY 10001',
        streetAddress: '123 Main Street',
        city: 'New York',
        state: 'NY',
        zip: '10001',
        lat: position.lat ? position.lat() : 40.7128,
        lng: position.lng ? position.lng() : -74.0060
      };
      
      console.log('📍 Mock address selected:', mockAddress);
      setSelectedAddress(mockAddress);
    }, 1000);
  };

  const handleConfirmAddress = () => {
    if (selectedAddress) {
      onAddressSelect(selectedAddress);
    }
  };

  const handleSearchLocation = (searchQuery) => {
    if (!map || !searchQuery.trim()) return;

    console.log('🗺️ Mock search for address:', searchQuery);
    
    // Mock search for demo purposes
    setTimeout(() => {
      const mockPosition = { lat: () => 40.7128, lng: () => -74.0060 };
      console.log('📍 Mock search result:', mockPosition);
      reverseGeocode(mockPosition);
    }, 1000);
  };

  return (
    <div className="map-address-selector">
      <div className="map-header">
        <h3>Select Address from Map</h3>
        <button className="close-button" onClick={onClose}>✕</button>
      </div>
      
      <div className="search-container">
        <input
          type="text"
          placeholder="Search for an address..."
          className="address-search"
          onKeyPress={(e) => {
            if (e.key === 'Enter') {
              handleSearchLocation(e.target.value);
            }
          }}
        />
        <button 
          className="search-button"
          onClick={() => {
            const input = document.querySelector('.address-search');
            handleSearchLocation(input.value);
          }}
        >
          🔍
        </button>
      </div>

      <div className="map-container">
        {isLoading && (
          <div className="map-loading">
            <div className="loading-spinner"></div>
            <p>Loading map...</p>
          </div>
        )}
        <div ref={mapRef} className="google-map" style={{
          width: '100%',
          height: '500px',
          border: '3px solid #007bff',
          background: '#f9f9f9',
          position: 'relative',
          display: 'block',
          minHeight: '500px'
        }}>
          <div className="mock-map" onClick={() => {
            console.log('🗺️ Mock map clicked!');
            const mockPosition = { lat: () => 40.7128, lng: () => -74.0060 };
            reverseGeocode(mockPosition);
          }} style={{
            width: '100%',
            height: '100%',
            minHeight: '500px',
            background: 'linear-gradient(45deg, #f0f0f0 25%, transparent 25%), linear-gradient(-45deg, #f0f0f0 25%, transparent 25%), linear-gradient(45deg, transparent 75%, #f0f0f0 75%), linear-gradient(-45deg, transparent 75%, #f0f0f0 75%)',
            backgroundSize: '20px 20px',
            backgroundPosition: '0 0, 0 10px, 10px -10px, -10px 0px',
            cursor: 'pointer',
            position: 'relative',
            border: '2px solid #ddd',
            borderRadius: '8px',
            display: 'block',
            overflow: 'visible'
          }}>
            <div className="mock-map-content" style={{
              width: '100%',
              height: '100%',
              minHeight: '500px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              background: 'rgba(255, 255, 255, 0.9)',
              padding: '20px',
              position: 'relative',
              zIndex: 1
            }}>
              <div className="mock-map-placeholder">
                <div className="map-icon">🗺️</div>
                <h4>Interactive Map (Demo Mode)</h4>
                <p>Click anywhere on the map to select an address</p>
                <p className="demo-note">(Mock Implementation - No Billing Required)</p>
                <div className="api-note">
                  <p><strong>For Real Google Maps:</strong></p>
                  <ol>
                    <li>Enable billing in Google Cloud Console</li>
                    <li>Use a valid API key with billing enabled</li>
                    <li>Replace mock implementation with real API calls</li>
                  </ol>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {selectedAddress && (
        <div className="selected-address">
          <h4>Selected Address:</h4>
          <p>{selectedAddress.fullAddress}</p>
          <div className="address-details">
            <span><strong>Street:</strong> {selectedAddress.streetAddress}</span>
            <span><strong>City:</strong> {selectedAddress.city}</span>
            <span><strong>State:</strong> {selectedAddress.state}</span>
            <span><strong>ZIP:</strong> {selectedAddress.zip}</span>
          </div>
        </div>
      )}

      <div className="map-actions">
        <button 
          className="cancel-button" 
          onClick={onClose}
        >
          Cancel
        </button>
        <button 
          className="confirm-button" 
          onClick={handleConfirmAddress}
          disabled={!selectedAddress}
        >
          Confirm Address
        </button>
      </div>
    </div>
  );
};

export default MapAddressSelector; 