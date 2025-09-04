import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import SideMenu from './SideMenu.jsx';
import './AppLayout.css';
import logo from '../assets/logo.svg';

const AppLayout = ({ children, user, handleLogout }) => {
  const [isSideMenuOpen, setIsSideMenuOpen] = useState(false);
  const navigate = useNavigate();

  const toggleSideMenu = () => {
    setIsSideMenuOpen(!isSideMenuOpen);
  };

  const closeSideMenu = () => {
    setIsSideMenuOpen(false);
  };

  return (
    <div className="app-layout">
      {/* Header */}
      <header className="App-header">
        <div className="user-info">
          <div className="logo" onClick={() => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
          }} style={{ cursor: 'pointer' }}>
            <img src={logo} alt="We Know Logo" className="landing-logo" />
          </div>
          <div className="header-right">
            <button className="hamburger-menu-button" onClick={toggleSideMenu}>
              <div className="hamburger-icon">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </button>
          </div>
        </div>
        
        <div className="title-container">
          <div className="title-background" onClick={() => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
          }} style={{ cursor: 'pointer' }}>
            <h1 className="main-title">We Know</h1>
            <p className="title-subtitle">Get fresh ingredients delivered for any dish</p>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="app-main">
        {children}
      </main>

      {/* Side Menu */}
      <SideMenu
        user={user}
        isOpen={isSideMenuOpen}
        onClose={closeSideMenu}
        onLogout={handleLogout}
        onNavigateToProfile={() => {}}
        onNavigateToSettings={() => {}}
      />
    </div>
  );
};

export default AppLayout; 