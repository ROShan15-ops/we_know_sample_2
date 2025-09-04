import React, { useState } from 'react';
import ProfileContainer from './ProfileContainer';
import './ProfileDemo.css';

const ProfileDemo = () => {
  const [user, setUser] = useState({
    id: 'WK001',
    name: 'John Doe',
    email: 'john.doe@example.com',
    phone: '+1 (555) 123-4567',
    created_at: '2024-01-15T10:30:00Z',
    last_login: '2024-07-29T14:20:00Z'
  });

  const handleLogout = () => {
    alert('Logout Successful! You have been logged out successfully.');
    console.log('User logged out');
  };

  return (
    <div className="profile-demo-container">
      <ProfileContainer 
        user={user}
        onLogout={handleLogout}
      />
    </div>
  );
};

export default ProfileDemo; 