import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './SideMenu.css';
import AllergyManagementModal from './AllergyManagementModal.jsx';

const SideMenu = ({ user, isOpen, onClose, onLogout, onNavigateToProfile, onNavigateToSettings }) => {
  const navigate = useNavigate();
  const [showProfileEdit, setShowProfileEdit] = useState(false);
  const [showPasswordChange, setShowPasswordChange] = useState(false);
  const [showAllergyManagement, setShowAllergyManagement] = useState(false);

  const handleProfileEdit = () => {
    setShowProfileEdit(true);
    onClose(); // Close the side menu
  };

  const handlePasswordChange = () => {
    setShowPasswordChange(true);
    onClose(); // Close the side menu
  };

  const handleOrderHistory = () => {
    navigate('/order-history');
    onClose();
  };

  const handleSavedAddresses = () => {
    navigate('/saved-addresses');
    onClose();
  };

  const handleTrackOrders = () => {
    navigate('/track-orders');
    onClose();
  };

  const handleSettings = () => {
    navigate('/settings');
    onClose();
  };

  const handleNotifications = () => {
    navigate('/notifications');
    onClose();
  };

  const handlePaymentMethods = () => {
    navigate('/payment-methods');
    onClose();
  };

  const handleHelpSupport = () => {
    navigate('/help-support');
    onClose();
  };

  const handleContactUs = () => {
    navigate('/contact-us');
    onClose();
  };

  const handleRateApp = () => {
    navigate('/rate-app');
    onClose();
  };

  const handleTermsOfService = () => {
    navigate('/terms');
    onClose();
  };

  const handlePrivacyPolicy = () => {
    navigate('/privacy-policy');
    onClose();
  };

  const handleAllergyManagement = () => {
    setShowAllergyManagement(true);
    onClose(); // Close the side menu
  };

  const handleLogout = () => {
    if (window.confirm('Are you sure you want to logout?')) {
      onLogout();
    }
  };

  return (
    <>
      {/* Overlay */}
      {isOpen && (
        <div className="side-menu-overlay" onClick={onClose}></div>
      )}

      {/* Side Menu */}
      <div className={`side-menu ${isOpen ? 'open' : ''}`}>
        {/* Header */}
        <div className="side-menu-header">
          <div className="user-info">
            <div className="user-avatar">
              {user?.profileImage ? (
                <img src={user.profileImage} alt="Profile" />
              ) : (
                <div className="avatar-placeholder">
                  {user?.name?.charAt(0) || 'U'}
                </div>
              )}
            </div>
            <div className="user-details">
              <h3 className="user-name">{user?.name || 'User Name'}</h3>
              <p className="user-email">{user?.email || 'user@example.com'}</p>
            </div>
          </div>
          <button className="close-button" onClick={onClose}>
            ✕
          </button>
        </div>

        {/* Menu Items */}
        <div className="side-menu-content">
          <div className="menu-section">
            <h4 className="section-title">Account</h4>
            
            <button className="menu-item" onClick={handleProfileEdit}>
              <div className="menu-icon">👤</div>
              <div className="menu-text">
                <div className="menu-title">Edit Profile</div>
                <div className="menu-subtitle">Change your name and details</div>
              </div>
              <div className="chevron">›</div>
            </button>

            <button className="menu-item" onClick={handlePasswordChange}>
              <div className="menu-icon">🔒</div>
              <div className="menu-text">
                <div className="menu-title">Change Password</div>
                <div className="menu-subtitle">Update your password</div>
              </div>
              <div className="chevron">›</div>
            </button>

            <button className="menu-item" onClick={onNavigateToProfile}>
              <div className="menu-icon">📋</div>
              <div className="menu-text">
                <div className="menu-title">My Profile</div>
                <div className="menu-subtitle">View your complete profile</div>
              </div>
              <div className="chevron">›</div>
            </button>
          </div>

          <div className="menu-section">
            <h4 className="section-title">Orders & Delivery</h4>
            
            <button className="menu-item" onClick={handleOrderHistory}>
              <div className="menu-icon">📦</div>
              <div className="menu-text">
                <div className="menu-title">Order History</div>
                <div className="menu-subtitle">View your past orders</div>
              </div>
              <div className="chevron">›</div>
            </button>

            <button className="menu-item" onClick={handleSavedAddresses}>
              <div className="menu-icon">📍</div>
              <div className="menu-text">
                <div className="menu-title">Saved Addresses</div>
                <div className="menu-subtitle">Manage delivery addresses</div>
              </div>
              <div className="chevron">›</div>
            </button>

            <button className="menu-item" onClick={handleTrackOrders}>
              <div className="menu-icon">🚚</div>
              <div className="menu-text">
                <div className="menu-title">Track Orders</div>
                <div className="menu-subtitle">Track current deliveries</div>
              </div>
              <div className="chevron">›</div>
            </button>
          </div>

          <div className="menu-section">
            <h4 className="section-title">Preferences</h4>
            
            <button className="menu-item" onClick={handleSettings}>
              <div className="menu-icon">⚙️</div>
              <div className="menu-text">
                <div className="menu-title">Settings</div>
                <div className="menu-subtitle">Notifications, language, theme</div>
              </div>
              <div className="chevron">›</div>
            </button>

            <button className="menu-item" onClick={handleNotifications}>
              <div className="menu-icon">🔔</div>
              <div className="menu-text">
                <div className="menu-title">Notifications</div>
                <div className="menu-subtitle">Manage push notifications</div>
              </div>
              <div className="chevron">›</div>
            </button>

            <button className="menu-item" onClick={handlePaymentMethods}>
              <div className="menu-icon">💳</div>
              <div className="menu-text">
                <div className="menu-title">Payment Methods</div>
                <div className="menu-subtitle">Manage saved cards</div>
              </div>
              <div className="chevron">›</div>
            </button>

            <button className="menu-item" onClick={handleAllergyManagement}>
              <div className="menu-icon">⚠️</div>
              <div className="menu-text">
                <div className="menu-title">Manage Allergies</div>
                <div className="menu-subtitle">Update your allergy profile</div>
              </div>
              <div className="chevron">›</div>
            </button>
          </div>

          <div className="menu-section">
            <h4 className="section-title">Support</h4>
            
            <button className="menu-item" onClick={handleHelpSupport}>
              <div className="menu-icon">❓</div>
              <div className="menu-text">
                <div className="menu-title">Help & Support</div>
                <div className="menu-subtitle">Get help with your account</div>
              </div>
              <div className="chevron">›</div>
            </button>

            <button className="menu-item" onClick={handleContactUs}>
              <div className="menu-icon">📞</div>
              <div className="menu-text">
                <div className="menu-title">Contact Us</div>
                <div className="menu-subtitle">Reach out to our team</div>
              </div>
              <div className="chevron">›</div>
            </button>

            <button className="menu-item" onClick={handleRateApp}>
              <div className="menu-icon">⭐</div>
              <div className="menu-text">
                <div className="menu-title">Rate App</div>
                <div className="menu-subtitle">Rate us on app store</div>
              </div>
              <div className="chevron">›</div>
            </button>
          </div>

          <div className="menu-section">
            <h4 className="section-title">Legal</h4>
            
            <button className="menu-item" onClick={handleTermsOfService}>
              <div className="menu-icon">📄</div>
              <div className="menu-text">
                <div className="menu-title">Terms of Service</div>
                <div className="menu-subtitle">Read our terms</div>
              </div>
              <div className="chevron">›</div>
            </button>

            <button className="menu-item" onClick={handlePrivacyPolicy}>
              <div className="menu-icon">🛡️</div>
              <div className="menu-text">
                <div className="menu-title">Privacy Policy</div>
                <div className="menu-subtitle">Read our privacy policy</div>
              </div>
              <div className="chevron">›</div>
            </button>
          </div>
        </div>

        {/* Footer */}
        <div className="side-menu-footer">
          <button className="logout-button" onClick={handleLogout}>
            <div className="menu-icon">🚪</div>
            <div className="menu-text">
              <div className="menu-title">Logout</div>
              <div className="menu-subtitle">Sign out of your account</div>
            </div>
          </button>
          
          <div className="app-version">
            We Know v1.0.0
          </div>
        </div>
      </div>

      {/* Profile Edit Modal */}
      {showProfileEdit && (
        <ProfileEditModal 
          user={user}
          onClose={() => setShowProfileEdit(false)}
        />
      )}

              {/* Password Change Modal */}
        {showPasswordChange && (
          <PasswordChangeModal 
            onClose={() => setShowPasswordChange(false)}
          />
        )}

        {/* Profile Edit Modal */}
        {showProfileEdit && (
          <ProfileEditModal 
            user={user}
            onClose={() => setShowProfileEdit(false)}
          />
        )}

        {/* Allergy Management Modal */}
        {showAllergyManagement && (
          <AllergyManagementModal 
            user={user}
            isOpen={showAllergyManagement}
            onClose={() => setShowAllergyManagement(false)}
          />
        )}
      </>
    );
  };

// Profile Edit Modal Component
const ProfileEditModal = ({ user, onClose }) => {
  const [formData, setFormData] = useState({
    name: user?.name || '',
    email: user?.email || '',
    phone: user?.phone || ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    // TODO: Implement profile update logic
    alert('Profile updated successfully!');
    onClose();
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h3>Edit Profile</h3>
          <button className="close-button" onClick={onClose}>✕</button>
        </div>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Full Name</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              placeholder="Enter your full name"
            />
          </div>
          
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              placeholder="Enter your email"
            />
          </div>
          
          <div className="form-group">
            <label>Phone Number</label>
            <input
              type="tel"
              value={formData.phone}
              onChange={(e) => setFormData({...formData, phone: e.target.value})}
              placeholder="Enter your phone number"
            />
          </div>
          
          <div className="modal-actions">
            <button type="button" className="cancel-button" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="save-button">
              Save Changes
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

// Password Change Modal Component
const PasswordChangeModal = ({ onClose }) => {
  const [formData, setFormData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.newPassword !== formData.confirmPassword) {
      alert('New passwords do not match!');
      return;
    }
    // TODO: Implement password change logic
    alert('Password changed successfully!');
    onClose();
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h3>Change Password</h3>
          <button className="close-button" onClick={onClose}>✕</button>
        </div>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Current Password</label>
            <input
              type="password"
              value={formData.currentPassword}
              onChange={(e) => setFormData({...formData, currentPassword: e.target.value})}
              placeholder="Enter current password"
            />
          </div>
          
          <div className="form-group">
            <label>New Password</label>
            <input
              type="password"
              value={formData.newPassword}
              onChange={(e) => setFormData({...formData, newPassword: e.target.value})}
              placeholder="Enter new password"
            />
          </div>
          
          <div className="form-group">
            <label>Confirm New Password</label>
            <input
              type="password"
              value={formData.confirmPassword}
              onChange={(e) => setFormData({...formData, confirmPassword: e.target.value})}
              placeholder="Confirm new password"
            />
          </div>
          
          <div className="modal-actions">
            <button type="button" className="cancel-button" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="save-button">
              Change Password
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};



export default SideMenu; 