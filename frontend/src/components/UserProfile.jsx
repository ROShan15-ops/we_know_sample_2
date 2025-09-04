import React, { useState } from 'react';
import './UserProfile.css';

const UserProfile = ({ onNavigateToSettings, onLogout, user }) => {
  const [profileImage, setProfileImage] = useState(null);

  const handleEditProfile = () => {
    // TODO: Implement edit profile functionality
    alert('Edit profile functionality will be implemented here');
  };

  const handleViewAddresses = () => {
    // TODO: Implement saved addresses view
    alert('Saved addresses functionality will be implemented here');
  };

  const handleViewOrderHistory = () => {
    // TODO: Implement order history view
    alert('Order history functionality will be implemented here');
  };

  const handleLogout = () => {
    if (window.confirm('Are you sure you want to logout?')) {
      onLogout();
    }
  };

  return (
    <div className="profile-container">
      {/* Header */}
      <div className="profile-header">
        <h1 className="header-title">Profile</h1>
        <button 
          className="settings-button"
          onClick={onNavigateToSettings}
        >
          ⚙️
        </button>
      </div>

      {/* Profile Section */}
      <div className="profile-section">
        {/* Avatar */}
        <div className="avatar-container">
          {profileImage ? (
            <img src={profileImage} alt="Profile" className="avatar" />
          ) : (
            <div className="avatar-placeholder">
              👤
            </div>
          )}
          <button className="edit-avatar-button">
            ✏️
          </button>
        </div>

        {/* User Info */}
        <div className="user-info">
          <h2 className="user-name">{user?.name || 'User Name'}</h2>
          <div className="contact-info">
            📧 {user?.email || 'user@example.com'}
          </div>
          <div className="contact-info">
            📞 +1 (555) 123-4567
          </div>
        </div>

        {/* Edit Profile Button */}
        <button className="edit-profile-button" onClick={handleEditProfile}>
          ✏️ Edit Profile
        </button>
      </div>

      {/* Menu Items */}
      <div className="menu-section">
        <button className="menu-item" onClick={handleViewAddresses}>
          <div className="menu-item-left">
            <div className="menu-icon">📍</div>
            <div className="menu-text-container">
              <div className="menu-title">Saved Addresses</div>
              <div className="menu-subtitle">Manage your delivery addresses</div>
            </div>
          </div>
          <div className="chevron">›</div>
        </button>

        <button className="menu-item" onClick={handleViewOrderHistory}>
          <div className="menu-item-left">
            <div className="menu-icon">🕒</div>
            <div className="menu-text-container">
              <div className="menu-title">Order History</div>
              <div className="menu-subtitle">View your past orders</div>
            </div>
          </div>
          <div className="chevron">›</div>
        </button>
      </div>

      {/* Logout Section */}
      <div className="logout-section">
        <button className="logout-button" onClick={handleLogout}>
          🚪 Logout
        </button>
      </div>

      {/* App Version */}
      <div className="version-section">
        <div className="version-text">We Know v1.0.0</div>
      </div>
    </div>
  );
};

export default UserProfile; 