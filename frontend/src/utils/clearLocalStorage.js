// Utility function to clear all localStorage data
export const clearAllLocalStorage = () => {
  // Clear all keys that start with 'weKnow'
  const keysToRemove = [];
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (key && key.startsWith('weKnow')) {
      keysToRemove.push(key);
    }
  }
  keysToRemove.forEach(key => {
    console.log('Removing localStorage key:', key);
    localStorage.removeItem(key);
  });
  
  console.log('All weKnow localStorage data cleared');
};

// Function to log all current localStorage data
export const logLocalStorageData = () => {
  console.log('Current localStorage data:');
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (key && key.startsWith('weKnow')) {
      console.log(`${key}:`, localStorage.getItem(key));
    }
  }
}; 