import React, { useState } from 'react';
import UserProfile from './UserProfile';
import UserSettings from './UserSettings';

const ProfileContainer = ({ user, onLogout }) => {
  const [currentView, setCurrentView] = useState('profile'); // 'profile' or 'settings'

  const handleNavigateToSettings = () => {
    setCurrentView('settings');
  };

  const handleBackToProfile = () => {
    setCurrentView('profile');
  };

  const handleLogout = () => {
    // Call the parent's logout function
    onLogout();
  };

  return (
    <div className="profile-container-wrapper">
      {currentView === 'profile' ? (
        <UserProfile
          user={user}
          onNavigateToSettings={handleNavigateToSettings}
          onLogout={handleLogout}
        />
      ) : (
        <UserSettings
          user={user}
          onBack={handleBackToProfile}
        />
      )}
    </div>
  );
};

export default ProfileContainer; 