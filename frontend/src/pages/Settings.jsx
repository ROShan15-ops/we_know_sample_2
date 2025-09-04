import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Pages.css';

const Settings = () => {
  const [settings, setSettings] = useState({
    notifications: {
      push: true,
      email: true,
      sms: false
    },
    language: 'English',
    theme: 'Light',
    autoSave: true
  });

  const handleToggleSetting = (category, setting) => {
    setSettings(prev => ({
      ...prev,
      [category]: {
        ...prev[category],
        [setting]: !prev[category][setting]
      }
    }));
  };

  const handleChangeSetting = (category, value) => {
    setSettings(prev => ({
      ...prev,
      [category]: value
    }));
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <Link to="/" className="back-button">
          ← Back to Home
        </Link>
        <h1>Settings</h1>
      </div>

      <div className="page-content">
        <div className="settings-sections">
          
          {/* Notifications Section */}
          <div className="settings-section">
            <h3>Notifications</h3>
            <div className="setting-item">
              <div className="setting-info">
                <h4>Push Notifications</h4>
                <p>Receive notifications about orders and deliveries</p>
              </div>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={settings.notifications.push}
                  onChange={() => handleToggleSetting('notifications', 'push')}
                />
                <span className="toggle-slider"></span>
              </label>
            </div>

            <div className="setting-item">
              <div className="setting-info">
                <h4>Email Notifications</h4>
                <p>Get order updates via email</p>
              </div>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={settings.notifications.email}
                  onChange={() => handleToggleSetting('notifications', 'email')}
                />
                <span className="toggle-slider"></span>
              </label>
            </div>

            <div className="setting-item">
              <div className="setting-info">
                <h4>SMS Notifications</h4>
                <p>Receive text messages for urgent updates</p>
              </div>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={settings.notifications.sms}
                  onChange={() => handleToggleSetting('notifications', 'sms')}
                />
                <span className="toggle-slider"></span>
              </label>
            </div>
          </div>

          {/* App Preferences Section */}
          <div className="settings-section">
            <h3>App Preferences</h3>
            
            <div className="setting-item">
              <div className="setting-info">
                <h4>Language</h4>
                <p>Choose your preferred language</p>
              </div>
              <select
                value={settings.language}
                onChange={(e) => handleChangeSetting('language', e.target.value)}
                className="setting-select"
              >
                <option value="English">English</option>
                <option value="Spanish">Spanish</option>
                <option value="French">French</option>
                <option value="German">German</option>
              </select>
            </div>

            <div className="setting-item">
              <div className="setting-info">
                <h4>Theme</h4>
                <p>Choose your preferred theme</p>
              </div>
              <select
                value={settings.theme}
                onChange={(e) => handleChangeSetting('theme', e.target.value)}
                className="setting-select"
              >
                <option value="Light">Light</option>
                <option value="Dark">Dark</option>
                <option value="Auto">Auto</option>
              </select>
            </div>

            <div className="setting-item">
              <div className="setting-info">
                <h4>Auto-save</h4>
                <p>Automatically save your preferences</p>
              </div>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={settings.autoSave}
                  onChange={() => handleChangeSetting('autoSave', !settings.autoSave)}
                />
                <span className="toggle-slider"></span>
              </label>
            </div>
          </div>

          {/* Account Section */}
          <div className="settings-section">
            <h3>Account</h3>
            
            <div className="setting-item">
              <div className="setting-info">
                <h4>Privacy</h4>
                <p>Manage your privacy settings</p>
              </div>
              <Link to="/privacy" className="setting-link">
                Manage →
              </Link>
            </div>

            <div className="setting-item">
              <div className="setting-info">
                <h4>Security</h4>
                <p>Change password and security settings</p>
              </div>
              <Link to="/security" className="setting-link">
                Manage →
              </Link>
            </div>

            <div className="setting-item">
              <div className="setting-info">
                <h4>Data Usage</h4>
                <p>Manage your data and storage</p>
              </div>
              <Link to="/data" className="setting-link">
                Manage →
              </Link>
            </div>
          </div>

          {/* About Section */}
          <div className="settings-section">
            <h3>About</h3>
            
            <div className="setting-item">
              <div className="setting-info">
                <h4>App Version</h4>
                <p>We Know v1.0.0</p>
              </div>
            </div>

            <div className="setting-item">
              <div className="setting-info">
                <h4>Terms of Service</h4>
                <p>Read our terms and conditions</p>
              </div>
              <Link to="/terms" className="setting-link">
                View →
              </Link>
            </div>

            <div className="setting-item">
              <div className="setting-info">
                <h4>Privacy Policy</h4>
                <p>Learn how we protect your data</p>
              </div>
              <Link to="/privacy-policy" className="setting-link">
                View →
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings; 