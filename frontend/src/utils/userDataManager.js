// User Data Manager - Handles user-specific data storage
class UserDataManager {
  constructor() {
    this.currentUserId = null;
  }

  // Set current user ID
  setCurrentUser(userId) {
    this.currentUserId = userId;
  }

  // Get current user ID
  getCurrentUserId() {
    if (!this.currentUserId) {
      const user = localStorage.getItem('weKnowUser');
      if (user) {
        const userData = JSON.parse(user);
        this.currentUserId = userData.id || userData.email;
      }
    }
    return this.currentUserId;
  }

  // Generate user-specific key
  getUserKey(key) {
    const userId = this.getCurrentUserId();
    return userId ? `${key}_${userId}` : key;
  }

  // Save data for current user
  saveUserData(key, data) {
    const userKey = this.getUserKey(key);
    localStorage.setItem(userKey, JSON.stringify(data));
  }

  // Load data for current user
  loadUserData(key, defaultValue = null) {
    const userKey = this.getUserKey(key);
    const saved = localStorage.getItem(userKey);
    return saved ? JSON.parse(saved) : defaultValue;
  }

  // Remove data for current user
  removeUserData(key) {
    const userKey = this.getUserKey(key);
    localStorage.removeItem(userKey);
  }

  // Clear all data for current user
  clearCurrentUserData() {
    const userId = this.getCurrentUserId();
    if (userId) {
      // Remove all keys that start with the user ID
      const keysToRemove = [];
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key && key.includes(`_${userId}`)) {
          keysToRemove.push(key);
        }
      }
      keysToRemove.forEach(key => localStorage.removeItem(key));
    }
  }

  // Get all data for a specific user (for admin purposes)
  getAllUserData(userId) {
    const userData = {};
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.includes(`_${userId}`)) {
        const baseKey = key.replace(`_${userId}`, '');
        userData[baseKey] = JSON.parse(localStorage.getItem(key));
      }
    }
    return userData;
  }

  // Check if user has any data
  hasUserData() {
    const userId = this.getCurrentUserId();
    if (!userId) return false;
    
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.includes(`_${userId}`)) {
        return true;
      }
    }
    return false;
  }
}

// Create singleton instance
const userDataManager = new UserDataManager();

export default userDataManager; 