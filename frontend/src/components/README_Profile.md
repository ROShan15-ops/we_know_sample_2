# We Know - Profile & Settings UI Components

This directory contains React Native components for the user profile and settings functionality of the We Know food delivery app.

## Components Overview

### 1. UserProfile.jsx
The main profile screen component that displays user information and provides navigation to various features.

**Features:**
- User avatar with edit functionality
- User name and contact information display
- Edit profile button
- Saved addresses access
- Order history access
- Logout functionality
- Settings navigation

**Props:**
- `user` (object): User data containing id, name, email, etc.
- `onNavigateToSettings` (function): Callback to navigate to settings
- `onLogout` (function): Callback to handle logout

### 2. UserSettings.jsx
The settings screen component that provides various app configuration options.

**Features:**
- Notification preferences toggle
- Language selection (dropdown placeholder)
- Dark mode toggle
- Security settings (password reset, 2FA)
- Help & support access
- Privacy policy and terms of service
- App version information
- Account information display

**Props:**
- `onBack` (function): Callback to navigate back to profile
- `user` (object): User data for account information

### 3. ProfileContainer.jsx
A container component that manages navigation between profile and settings views.

**Features:**
- State management for view switching
- Seamless navigation between profile and settings
- Props forwarding to child components

**Props:**
- `user` (object): User data
- `onLogout` (function): Logout callback

### 4. ProfileDemo.jsx
A demo component showcasing the profile and settings functionality with mock data.

**Features:**
- Mock user data
- Logout simulation
- Complete UI demonstration

## Styling

All components use modern, mobile-friendly styling with:
- Flexbox layout
- Consistent color scheme
- Proper spacing and typography
- Touch-friendly button sizes
- Smooth transitions and animations

## Color Scheme

- **Primary Blue**: #007AFF
- **Secondary Orange**: #FF6B35
- **Success Green**: #00B894
- **Warning Orange**: #FFA726
- **Error Red**: #FF3B30
- **Purple**: #6C5CE7
- **Background**: #f8f9fa
- **Text Primary**: #333
- **Text Secondary**: #666
- **Border**: #e9ecef

## Icons

The components use Feather icons from `react-native-feather`:
- User, Edit3, MapPin, Clock, LogOut, Settings
- ArrowLeft, Bell, Globe, Moon, Shield, HelpCircle
- Info, ChevronRight, Lock, Smartphone

## Usage Example

```jsx
import ProfileContainer from './components/ProfileContainer';

const App = () => {
  const user = {
    id: 'WK001',
    name: 'John Doe',
    email: 'john.doe@example.com'
  };

  const handleLogout = () => {
    // Handle logout logic
    console.log('User logged out');
  };

  return (
    <ProfileContainer 
      user={user}
      onLogout={handleLogout}
    />
  );
};
```

## Features Implemented

### Profile Screen
✅ User avatar with edit button
✅ Username and contact info display
✅ Edit profile button
✅ Saved addresses access
✅ Order history access
✅ Logout button with confirmation
✅ Settings navigation

### Settings Screen
✅ Notification preferences toggle
✅ Language selection (placeholder)
✅ Dark mode toggle
✅ Password reset functionality
✅ Two-factor authentication (placeholder)
✅ Help & support access
✅ Privacy policy and terms links
✅ App version information
✅ Account information display

## Future Enhancements

- [ ] Image picker for avatar upload
- [ ] Language selection modal
- [ ] Dark mode theme implementation
- [ ] Two-factor authentication setup
- [ ] Real API integration for settings
- [ ] Push notification configuration
- [ ] Address management screen
- [ ] Order history screen
- [ ] Profile editing screen

## Dependencies

- `react-native-feather`: For icons
- `react-native`: Core React Native components
- `@react-native-async-storage/async-storage`: For settings persistence (future)

## Installation

Make sure to install the required dependencies:

```bash
npm install react-native-feather
```

## Notes

- All components are designed for mobile-first experience
- Components use functional components with hooks
- Styling follows React Native best practices
- Components are reusable and modular
- Error handling and loading states are implemented
- Accessibility features are considered in the design 