import React, { useState } from 'react';
import SideMenu from './SideMenu';
import './HeaderWithMenu.css';

const HeaderWithMenu = ({ user, onLogout, onNavigateToProfile, onNavigateToSettings }) => {
  const [isSideMenuOpen, setIsSideMenuOpen] = useState(false);

  const toggleSideMenu = () => {
    setIsSideMenuOpen(!isSideMenuOpen);
  };

  const closeSideMenu = () => {
    setIsSideMenuOpen(false);
  };

  const handleLogout = () => {
    closeSideMenu();
    onLogout();
  };

  const handleNavigateToProfile = () => {
    closeSideMenu();
    onNavigateToProfile();
  };

  const handleNavigateToSettings = () => {
    closeSideMenu();
    onNavigateToSettings();
  };

  return (
    <>
      {/* Header */}
      <header className="header-with-menu">
        <div className="header-content">
          {/* Logo */}
          <div className="header-logo">
            <h1 className="logo-text">We Know</h1>
          </div>

          {/* Search Bar */}
          <div className="header-search">
            <div className="search-container">
              <span className="search-icon">🔍</span>
              <input
                type="text"
                placeholder="Search for dishes, ingredients..."
                className="search-input"
              />
            </div>
          </div>

          {/* User Menu */}
          <div className="header-user-menu">
            {/* User Avatar */}
            <button className="user-avatar-button" onClick={toggleSideMenu}>
              {user?.profileImage ? (
                <img src={user.profileImage} alt="Profile" className="user-avatar" />
              ) : (
                <div className="user-avatar-placeholder">
                  {user?.name?.charAt(0) || 'U'}
                </div>
              )}
            </button>

            {/* Menu Toggle */}
            <button className="menu-toggle-button" onClick={toggleSideMenu}>
              <div className="hamburger">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </button>
          </div>
        </div>
      </header>

      {/* Side Menu */}
      <SideMenu
        user={user}
        isOpen={isSideMenuOpen}
        onClose={closeSideMenu}
        onLogout={handleLogout}
        onNavigateToProfile={handleNavigateToProfile}
        onNavigateToSettings={handleNavigateToSettings}
      />
    </>
  );
};

export default HeaderWithMenu; 