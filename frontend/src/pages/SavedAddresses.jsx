import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './Pages.css';

const SavedAddresses = () => {
  const [addresses, setAddresses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newAddress, setNewAddress] = useState({
    address_type: '',
    address_line1: '',
    address_line2: '',
    city: '',
    state: '',
    zip_code: '',
    is_default: false
  });

  // Fetch user's addresses from backend
  const fetchAddresses = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('weKnowToken');
      if (!token) {
        setError('Please login to view your addresses');
        setLoading(false);
        return;
      }

      const response = await axios.get('http://localhost:8000/user/addresses', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.data.success) {
        setAddresses(response.data.addresses || []);
      } else {
        setError('Failed to fetch addresses');
      }
    } catch (error) {
      console.error('Error fetching addresses:', error);
      setError('Failed to load addresses. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Add new address
  const handleAddAddress = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('weKnowToken');
      if (!token) {
        setError('Please login to add addresses');
        return;
      }

      const addressData = {
        ...newAddress,
        is_default: addresses.length === 0 || newAddress.is_default
      };

      const response = await axios.post('http://localhost:8000/user/addresses', addressData, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.data.success) {
        // Refresh addresses list
        await fetchAddresses();
        setNewAddress({
          address_type: '',
          address_line1: '',
          address_line2: '',
          city: '',
          state: '',
          zip_code: '',
          is_default: false
        });
        setShowAddForm(false);
      } else {
        setError('Failed to add address');
      }
    } catch (error) {
      console.error('Error adding address:', error);
      setError('Failed to add address. Please try again.');
    }
  };

  // Set address as default
  const handleSetDefault = async (addressId) => {
    try {
      const token = localStorage.getItem('weKnowToken');
      if (!token) {
        setError('Please login to modify addresses');
        return;
      }

      const response = await axios.put(`http://localhost:8000/user/addresses/${addressId}/default`, {}, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.data.success) {
        // Refresh addresses list to get updated data
        await fetchAddresses();
      } else {
        setError('Failed to set default address');
      }
    } catch (error) {
      console.error('Error setting default address:', error);
      setError('Failed to set default address');
    }
  };

  // Delete address
  const handleDeleteAddress = async (addressId) => {
    try {
      const token = localStorage.getItem('weKnowToken');
      if (!token) {
        setError('Please login to delete addresses');
        return;
      }

      const response = await axios.delete(`http://localhost:8000/user/addresses/${addressId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.data.success) {
        // Refresh addresses list to get updated data
        await fetchAddresses();
      } else {
        setError('Failed to delete address');
      }
    } catch (error) {
      console.error('Error deleting address:', error);
      setError('Failed to delete address');
    }
  };

  // Load addresses on component mount
  useEffect(() => {
    fetchAddresses();
  }, []);

  if (loading) {
    return (
      <div className="page-container">
        <div className="page-header">
          <Link to="/" className="back-button">
            ← Back to Home
          </Link>
          <h1>Saved Addresses</h1>
        </div>
        <div className="page-content">
          <div className="loading-state">
            <div className="loading-spinner"></div>
            <p>Loading your addresses...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <Link to="/" className="back-button">
          ← Back to Home
        </Link>
        <h1>Saved Addresses</h1>
        <button 
          className="add-button"
          onClick={() => setShowAddForm(true)}
        >
          + Add Address
        </button>
      </div>

      <div className="page-content">
        {error && (
          <div className="error-message">
            {error}
            <button onClick={() => setError(null)}>✕</button>
          </div>
        )}

        {addresses.length > 0 ? (
          <div className="addresses-list">
            {addresses.map((address) => (
              <div key={address.id} className="address-card">
                <div className="address-header">
                  <h3>{address.address_type}</h3>
                  {address.is_default && (
                    <span className="default-badge">Default</span>
                  )}
                </div>
                
                <div className="address-details">
                  <p>{address.address_line1}</p>
                  {address.address_line2 && <p>{address.address_line2}</p>}
                  <p>{address.city}, {address.state} {address.zip_code}</p>
                </div>

                <div className="address-actions">
                  {!address.is_default && (
                    <button 
                      className="action-button"
                      onClick={() => handleSetDefault(address.id)}
                    >
                      Set as Default
                    </button>
                  )}
                  <button 
                    className="action-button secondary"
                    onClick={() => handleDeleteAddress(address.id)}
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-icon">📍</div>
            <h3>No Saved Addresses</h3>
            <p>Add your delivery addresses for quick checkout</p>
            <button 
              className="cta-button"
              onClick={() => setShowAddForm(true)}
            >
              Add Your First Address
            </button>
          </div>
        )}

        {showAddForm && (
          <div className="modal-overlay">
            <div className="modal-content">
              <div className="modal-header">
                <h3>Add New Address</h3>
                <button 
                  className="close-button" 
                  onClick={() => setShowAddForm(false)}
                >
                  ✕
                </button>
              </div>
              
              <form onSubmit={handleAddAddress}>
                <div className="form-group">
                  <label>Address Type</label>
                  <select
                    value={newAddress.address_type}
                    onChange={(e) => setNewAddress({...newAddress, address_type: e.target.value})}
                    required
                  >
                    <option value="">Select address type</option>
                    <option value="home">Home</option>
                    <option value="work">Work</option>
                    <option value="other">Other</option>
                  </select>
                </div>
                
                <div className="form-group">
                  <label>Street Address</label>
                  <input
                    type="text"
                    value={newAddress.address_line1}
                    onChange={(e) => setNewAddress({...newAddress, address_line1: e.target.value})}
                    placeholder="Enter street address"
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label>Apartment/Suite (Optional)</label>
                  <input
                    type="text"
                    value={newAddress.address_line2}
                    onChange={(e) => setNewAddress({...newAddress, address_line2: e.target.value})}
                    placeholder="Apt, Suite, etc."
                  />
                </div>
                
                <div className="form-row">
                  <div className="form-group">
                    <label>City</label>
                    <input
                      type="text"
                      value={newAddress.city}
                      onChange={(e) => setNewAddress({...newAddress, city: e.target.value})}
                      placeholder="City"
                      required
                    />
                  </div>
                  
                  <div className="form-group">
                    <label>State</label>
                    <input
                      type="text"
                      value={newAddress.state}
                      onChange={(e) => setNewAddress({...newAddress, state: e.target.value})}
                      placeholder="State"
                      required
                    />
                  </div>
                  
                  <div className="form-group">
                    <label>ZIP Code</label>
                    <input
                      type="text"
                      value={newAddress.zip_code}
                      onChange={(e) => setNewAddress({...newAddress, zip_code: e.target.value})}
                      placeholder="ZIP"
                      required
                    />
                  </div>
                </div>
                
                <div className="form-group">
                  <label>
                    <input
                      type="checkbox"
                      checked={newAddress.is_default}
                      onChange={(e) => setNewAddress({...newAddress, is_default: e.target.checked})}
                    />
                    Set as default address
                  </label>
                </div>
                
                <div className="modal-actions">
                  <button 
                    type="button" 
                    className="cancel-button" 
                    onClick={() => setShowAddForm(false)}
                  >
                    Cancel
                  </button>
                  <button type="submit" className="save-button">
                    Add Address
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SavedAddresses; 