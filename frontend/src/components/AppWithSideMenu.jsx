import React, { useState } from 'react';
import HeaderWithMenu from './HeaderWithMenu';
import ProfileContainer from './ProfileContainer';
import './AppWithSideMenu.css';

const AppWithSideMenu = () => {
  const [currentView, setCurrentView] = useState('main'); // 'main', 'profile', 'settings'
  const [user, setUser] = useState({
    id: 'WK001',
    name: 'John Doe',
    email: 'john.doe@example.com',
    phone: '+1 (555) 123-4567',
    profileImage: null
  });

  const handleLogout = () => {
    // TODO: Implement actual logout logic
    alert('Logout successful!');
    console.log('User logged out');
  };

  const handleNavigateToProfile = () => {
    setCurrentView('profile');
  };

  const handleNavigateToSettings = () => {
    setCurrentView('settings');
  };

  const handleBackToMain = () => {
    setCurrentView('main');
  };

  // Main app content (your existing We Know app)
  const renderMainContent = () => (
    <div className="main-content">
      <div className="welcome-section">
        <h1>Welcome to We Know! 🍕</h1>
        <p>Your food delivery app with ingredient search and delivery</p>
      </div>
      
      <div className="features-grid">
        <div className="feature-card">
          <div className="feature-icon">🔍</div>
          <h3>Search Dishes</h3>
          <p>Find ingredients for any dish you want to cook</p>
        </div>
        
        <div className="feature-card">
          <div className="feature-icon">🚚</div>
          <h3>Get Delivery</h3>
          <p>Order fresh ingredients delivered to your door</p>
        </div>
        
        <div className="feature-card">
          <div className="feature-icon">📱</div>
          <h3>Track Orders</h3>
          <p>Track your delivery in real-time</p>
        </div>
        
        <div className="feature-card">
          <div className="feature-icon">👤</div>
          <h3>User Profile</h3>
          <p>Manage your account and preferences</p>
        </div>
      </div>
      
      <div className="demo-actions">
        <button 
          className="demo-button"
          onClick={handleNavigateToProfile}
        >
          👤 View Profile Demo
        </button>
        
        <button 
          className="demo-button"
          onClick={handleNavigateToSettings}
        >
          ⚙️ View Settings Demo
        </button>
      </div>
    </div>
  );

  // Profile view
  const renderProfileView = () => (
    <div className="profile-view">
      <div className="view-header">
        <button className="back-button" onClick={handleBackToMain}>
          ← Back to Main
        </button>
        <h2>Profile & Settings</h2>
      </div>
      <ProfileContainer 
        user={user}
        onLogout={handleLogout}
      />
    </div>
  );

  return (
    <div className="app-with-side-menu">
      {/* Header with Side Menu */}
      <HeaderWithMenu
        user={user}
        onLogout={handleLogout}
        onNavigateToProfile={handleNavigateToProfile}
        onNavigateToSettings={handleNavigateToSettings}
      />

      {/* Main Content */}
      <main className="app-main">
        {currentView === 'main' && renderMainContent()}
        {currentView === 'profile' && renderProfileView()}
        {currentView === 'settings' && renderProfileView()}
      </main>
    </div>
  );
};

export default AppWithSideMenu; 