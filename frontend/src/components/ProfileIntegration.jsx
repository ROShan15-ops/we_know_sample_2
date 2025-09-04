import React, { useState } from 'react';
import ProfileContainer from './ProfileContainer';
import './ProfileIntegration.css';

const ProfileIntegration = ({ currentUser, onLogout, onBackToMain }) => {
  const [showProfile, setShowProfile] = useState(false);

  const handleLogout = () => {
    // Handle logout logic here
    console.log('User logged out');
    onLogout();
  };

  const handleBackToMain = () => {
    setShowProfile(false);
    onBackToMain();
  };

  if (showProfile) {
    return (
      <div className="profile-integration">
        <ProfileContainer 
          user={currentUser}
          onLogout={handleLogout}
        />
      </div>
    );
  }

  return (
    <div className="profile-integration">
      <div className="profile-preview">
        <h2>Profile & Settings Components</h2>
        <p>Click the button below to see the profile and settings UI in action:</p>
        
        <button 
          className="view-profile-button"
          onClick={() => setShowProfile(true)}
        >
          👤 View Profile & Settings
        </button>
        
        <div className="features-list">
          <h3>Features Included:</h3>
          <ul>
            <li>✅ User avatar with edit functionality</li>
            <li>✅ Username and contact information</li>
            <li>✅ Edit profile button</li>
            <li>✅ Saved addresses access</li>
            <li>✅ Order history access</li>
            <li>✅ Logout functionality</li>
            <li>✅ Settings navigation</li>
            <li>✅ Notification preferences toggle</li>
            <li>✅ Language selection (placeholder)</li>
            <li>✅ Dark mode toggle</li>
            <li>✅ Security settings (password reset, 2FA)</li>
            <li>✅ Help & support access</li>
            <li>✅ Privacy policy and terms links</li>
            <li>✅ App version information</li>
            <li>✅ Account information display</li>
          </ul>
        </div>
        
        <button 
          className="back-button"
          onClick={handleBackToMain}
        >
          ← Back to Main App
        </button>
      </div>
    </div>
  );
};

export default ProfileIntegration; 