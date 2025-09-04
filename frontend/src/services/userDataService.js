import axios from 'axios';

// Base URL for API
const API_BASE_URL = 'http://localhost:8000';

// Helper function to get auth token
const getAuthToken = () => {
  return localStorage.getItem('weKnowToken');
};

// Helper function to get auth headers
const getAuthHeaders = () => {
  const token = getAuthToken();
  return {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  };
};

// User Data Service
class UserDataService {
  
  // Recent Searches
  async getRecentSearches() {
    try {
      const response = await axios.get(`${API_BASE_URL}/user/recent-searches`, {
        headers: getAuthHeaders()
      });
      return response.data.recent_searches || [];
    } catch (error) {
      console.error('Error fetching recent searches:', error);
      return [];
    }
  }

  async addRecentSearch(dishName) {
    try {
      await axios.post(`${API_BASE_URL}/user/recent-searches`, {
        dish_name: dishName
      }, {
        headers: getAuthHeaders()
      });
      return true;
    } catch (error) {
      console.error('Error adding recent search:', error);
      return false;
    }
  }

  // Orders
  async getOrders() {
    try {
      const response = await axios.get(`${API_BASE_URL}/user/orders`, {
        headers: getAuthHeaders()
      });
      return response.data.orders || [];
    } catch (error) {
      console.error('Error fetching orders:', error);
      return [];
    }
  }

  async addOrder(orderData) {
    try {
      const response = await axios.post(`${API_BASE_URL}/user/orders`, orderData, {
        headers: getAuthHeaders()
      });
      return response.data;
    } catch (error) {
      console.error('Error adding order:', error);
      throw error;
    }
  }

  async updateOrderStatus(orderId, status) {
    try {
      const response = await axios.put(`${API_BASE_URL}/user/orders/${orderId}/status`, {
        status: status
      }, {
        headers: getAuthHeaders()
      });
      return response.data;
    } catch (error) {
      console.error('Error updating order status:', error);
      throw error;
    }
  }

  async clearOrders() {
    try {
      const response = await axios.delete(`${API_BASE_URL}/user/orders/clear`, {
        headers: getAuthHeaders()
      });
      return response.data;
    } catch (error) {
      console.error('Error clearing orders:', error);
      throw error;
    }
  }

  // Addresses
  async getAddresses() {
    try {
      const response = await axios.get(`${API_BASE_URL}/user/addresses`, {
        headers: getAuthHeaders()
      });
      return response.data.addresses || [];
    } catch (error) {
      console.error('Error fetching addresses:', error);
      return [];
    }
  }

  async addAddress(addressData) {
    try {
      const response = await axios.post(`${API_BASE_URL}/user/addresses`, addressData, {
        headers: getAuthHeaders()
      });
      return response.data;
    } catch (error) {
      console.error('Error adding address:', error);
      throw error;
    }
  }

  // Preferences
  async getPreferences() {
    try {
      const response = await axios.get(`${API_BASE_URL}/user/preferences`, {
        headers: getAuthHeaders()
      });
      return response.data.preferences || {};
    } catch (error) {
      console.error('Error fetching preferences:', error);
      return {};
    }
  }

  async updatePreferences(preferencesData) {
    try {
      const response = await axios.put(`${API_BASE_URL}/user/preferences`, preferencesData, {
        headers: getAuthHeaders()
      });
      return response.data;
    } catch (error) {
      console.error('Error updating preferences:', error);
      throw error;
    }
  }

  // User Profile
  async getUserProfile() {
    try {
      const response = await axios.get(`${API_BASE_URL}/auth/me`, {
        headers: getAuthHeaders()
      });
      return response.data.user;
    } catch (error) {
      console.error('Error fetching user profile:', error);
      return null;
    }
  }

  // Check if user is authenticated
  isAuthenticated() {
    const token = getAuthToken();
    const user = localStorage.getItem('weKnowUser');
    return !!(token && user);
  }

  // Get current user data
  getCurrentUser() {
    const user = localStorage.getItem('weKnowUser');
    return user ? JSON.parse(user) : null;
  }

  // Clear user data on logout
  clearUserData() {
    localStorage.removeItem('weKnowToken');
    localStorage.removeItem('weKnowUser');
    // Clear any old localStorage keys that might interfere
    localStorage.removeItem('weKnowRecentSearches');
    localStorage.removeItem('weKnowAuthToken');
  }

  // Clear all app-related localStorage data
  clearAllAppData() {
    // Clear all keys that start with 'weKnow'
    const keysToRemove = [];
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.startsWith('weKnow')) {
        keysToRemove.push(key);
      }
    }
    keysToRemove.forEach(key => localStorage.removeItem(key));
  }
}

// Create singleton instance
const userDataService = new UserDataService();

export default userDataService; 