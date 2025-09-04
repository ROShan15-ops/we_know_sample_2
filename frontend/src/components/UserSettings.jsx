import React, { useState } from 'react';
import './UserSettings.css';

const UserSettings = ({ onBack, user }) => {
  const [notifications, setNotifications] = useState(true);
  const [darkMode, setDarkMode] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('English');

  const languages = [
    { code: 'en', name: 'English' },
    { code: 'es', name: 'Español' },
    { code: 'fr', name: 'Français' },
    { code: 'de', name: 'Deutsch' },
    { code: 'hi', name: 'हिंदी' },
    { code: 'zh', name: '中文' }
  ];

  const handleLanguageChange = () => {
    // TODO: Implement language selection modal
    alert('Language selection will be implemented here');
  };

  const handlePasswordReset = () => {
    if (window.confirm('A password reset link will be sent to your email address. Continue?')) {
      alert('Password reset link sent to your email!');
    }
  };

  const handleTwoFactorAuth = () => {
    if (window.confirm('Two-factor authentication setup will be implemented here. Continue?')) {
      alert('Two-factor authentication setup initiated!');
    }
  };

  const handleHelpSupport = () => {
    if (window.confirm('Would you like to contact our support team?')) {
      alert('Support contact functionality will be implemented here');
    }
  };

  const handlePrivacyPolicy = () => {
    // TODO: Open privacy policy URL
    alert('Privacy policy will be opened here');
  };

  const handleTermsOfService = () => {
    // TODO: Open terms of service URL
    alert('Terms of service will be opened here');
  };

  return (
    <div className="settings-container">
      {/* Header */}
      <div className="settings-header">
        <button className="back-button" onClick={onBack}>
          ←
        </button>
        <h1 className="header-title">Settings</h1>
        <div className="header-spacer"></div>
      </div>

      {/* Notifications Section */}
      <div className="settings-section">
        <h2 className="section-title">Notifications</h2>
        <div className="setting-item">
          <div className="setting-left">
            <div className="setting-icon">🔔</div>
            <div className="setting-text-container">
              <div className="setting-title">Push Notifications</div>
              <div className="setting-subtitle">Receive order updates and promotions</div>
            </div>
          </div>
          <label className="switch">
            <input
              type="checkbox"
              checked={notifications}
              onChange={(e) => setNotifications(e.target.checked)}
            />
            <span className="slider"></span>
          </label>
        </div>
      </div>

      {/* Preferences Section */}
      <div className="settings-section">
        <h2 className="section-title">Preferences</h2>
        
        <button className="setting-item" onClick={handleLanguageChange}>
          <div className="setting-left">
            <div className="setting-icon">🌐</div>
            <div className="setting-text-container">
              <div className="setting-title">Language</div>
              <div className="setting-subtitle">{selectedLanguage}</div>
            </div>
          </div>
          <div className="chevron">›</div>
        </button>

        <div className="setting-item">
          <div className="setting-left">
            <div className="setting-icon">🌙</div>
            <div className="setting-text-container">
              <div className="setting-title">Dark Mode</div>
              <div className="setting-subtitle">Switch to dark theme</div>
            </div>
          </div>
          <label className="switch">
            <input
              type="checkbox"
              checked={darkMode}
              onChange={(e) => setDarkMode(e.target.checked)}
            />
            <span className="slider"></span>
          </label>
        </div>
      </div>

      {/* Security Section */}
      <div className="settings-section">
        <h2 className="section-title">Security</h2>
        
        <button className="setting-item" onClick={handlePasswordReset}>
          <div className="setting-left">
            <div className="setting-icon">🔒</div>
            <div className="setting-text-container">
              <div className="setting-title">Reset Password</div>
              <div className="setting-subtitle">Change your account password</div>
            </div>
          </div>
          <div className="chevron">›</div>
        </button>

        <button className="setting-item" onClick={handleTwoFactorAuth}>
          <div className="setting-left">
            <div className="setting-icon">📱</div>
            <div className="setting-text-container">
              <div className="setting-title">Two-Factor Authentication</div>
              <div className="setting-subtitle">Add an extra layer of security</div>
            </div>
          </div>
          <div className="chevron">›</div>
        </button>
      </div>

      {/* Support Section */}
      <div className="settings-section">
        <h2 className="section-title">Support</h2>
        
        <button className="setting-item" onClick={handleHelpSupport}>
          <div className="setting-left">
            <div className="setting-icon">❓</div>
            <div className="setting-text-container">
              <div className="setting-title">Help & Support</div>
              <div className="setting-subtitle">Get help with your account</div>
            </div>
          </div>
          <div className="chevron">›</div>
        </button>

        <button className="setting-item" onClick={handlePrivacyPolicy}>
          <div className="setting-left">
            <div className="setting-icon">🛡️</div>
            <div className="setting-text-container">
              <div className="setting-title">Privacy Policy</div>
              <div className="setting-subtitle">Read our privacy policy</div>
            </div>
          </div>
          <div className="chevron">›</div>
        </button>

        <button className="setting-item" onClick={handleTermsOfService}>
          <div className="setting-left">
            <div className="setting-icon">📄</div>
            <div className="setting-text-container">
              <div className="setting-title">Terms of Service</div>
              <div className="setting-subtitle">Read our terms of service</div>
            </div>
          </div>
          <div className="chevron">›</div>
        </button>
      </div>

      {/* App Info Section */}
      <div className="settings-section">
        <h2 className="section-title">App Information</h2>
        
        <div className="setting-item">
          <div className="setting-left">
            <div className="setting-icon">ℹ️</div>
            <div className="setting-text-container">
              <div className="setting-title">Version</div>
              <div className="setting-subtitle">1.0.0</div>
            </div>
          </div>
        </div>

        <div className="setting-item">
          <div className="setting-left">
            <div className="setting-icon">ℹ️</div>
            <div className="setting-text-container">
              <div className="setting-title">Build Number</div>
              <div className="setting-subtitle">2024.1.0</div>
            </div>
          </div>
        </div>
      </div>

      {/* Account Info */}
      <div className="settings-section">
        <h2 className="section-title">Account Information</h2>
        
        <div className="setting-item">
          <div className="setting-left">
            <div className="setting-icon">🆔</div>
            <div className="setting-text-container">
              <div className="setting-title">User ID</div>
              <div className="setting-subtitle">{user?.id || 'N/A'}</div>
            </div>
          </div>
        </div>

        <div className="setting-item">
          <div className="setting-left">
            <div className="setting-icon">📅</div>
            <div className="setting-text-container">
              <div className="setting-title">Member Since</div>
              <div className="setting-subtitle">January 2024</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserSettings; 