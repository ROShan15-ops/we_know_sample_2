// Grocery Cart Service - Handles cart operations for different grocery apps

class GroceryCartService {
  constructor() {
    this.apps = {
      blinkit: {
        name: 'Blinkit',
        webCartUrl: 'https://blinkit.com/cart',
        appDeepLink: 'blinkit://cart',
        searchUrl: 'https://blinkit.com/search?q=',
        hasPublicAPI: false
      },
      zepto: {
        name: 'Zepto',
        webCartUrl: 'https://www.zepto.in/cart',
        appDeepLink: 'zepto://cart',
        searchUrl: 'https://www.zepto.in/search?q=',
        hasPublicAPI: false
      },
      bigbasket: {
        name: 'BigBasket',
        webCartUrl: 'https://www.bigbasket.com/cart',
        appDeepLink: 'bigbasket://cart',
        searchUrl: 'https://www.bigbasket.com/ps/?q=',
        hasPublicAPI: false
      }
    };
  }

  // Add ingredients to cart using the best available method
  async addToCart(appKey, ingredients) {
    const app = this.apps[appKey];
    if (!app) {
      throw new Error(`Unknown grocery app: ${appKey}`);
    }

    try {
      // Method 1: Try backend cart API first
      const apiResult = await this.addToCartViaAPI(appKey, ingredients);
      if (apiResult.success) {
        return apiResult;
      }

      // Method 2: Try mobile app deep link
      if (this.isMobileDevice()) {
        const deepLinkSuccess = await this.tryDeepLink(app.appDeepLink);
        if (deepLinkSuccess) {
          return { success: true, method: 'deep-link', message: `Opened ${app.name} app` };
        }
      }

      // Method 3: Try web cart with search parameters
      const webCartSuccess = await this.addToWebCart(app, ingredients);
      if (webCartSuccess) {
        return { success: true, method: 'web-cart', message: `Added to ${app.name} web cart` };
      }

      // Method 4: Fallback to search page
      return this.fallbackToSearch(app, ingredients);

    } catch (error) {
      console.error(`Error adding to ${app.name} cart:`, error);
      return this.fallbackToSearch(app, ingredients);
    }
  }

  // Add to cart via backend API
  async addToCartViaAPI(appKey, ingredients) {
    try {
      const response = await fetch('/cart/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          app_key: appKey,
          ingredients: ingredients,
          user_location: this.getUserLocation()
        })
      });

      if (response.ok) {
        const result = await response.json();
        return result;
      } else {
        throw new Error(`API request failed: ${response.status}`);
      }
    } catch (error) {
      console.error('Cart API error:', error);
      return { success: false, error: error.message };
    }
  }

  // Get user location (mock implementation)
  getUserLocation() {
    return {
      lat: 37.7749,
      lng: -122.4194
    };
  }

  // Check if user is on mobile device
  isMobileDevice() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
  }

  // Try to open mobile app via deep link
  async tryDeepLink(deepLink) {
    return new Promise((resolve) => {
      const timeout = setTimeout(() => {
        resolve(false);
      }, 2000);

      const originalHref = window.location.href;
      
      window.location.href = deepLink;
      
      // Check if app opened (user left the page)
      setTimeout(() => {
        if (window.location.href !== originalHref) {
          clearTimeout(timeout);
          resolve(true);
        }
      }, 1000);
    });
  }

  // Add items to web cart using URL parameters
  async addToWebCart(app, ingredients) {
    try {
      // Create cart URL with ingredients as search parameters
      const ingredientParams = ingredients.map(ingredient => {
        const name = typeof ingredient === 'string' 
          ? ingredient 
          : ingredient.ingredient || ingredient.name || '';
        return encodeURIComponent(name);
      }).join('&item=');

      const cartUrl = `${app.webCartUrl}?add=${ingredientParams}`;
      
      // Open cart page in new tab
      window.open(cartUrl, '_blank', 'noopener,noreferrer');
      
      return true;
    } catch (error) {
      console.error('Error adding to web cart:', error);
      return false;
    }
  }

  // Fallback to search page
  fallbackToSearch(app, ingredients) {
    const searchQuery = ingredients.map(ingredient => {
      const name = typeof ingredient === 'string' 
        ? ingredient 
        : ingredient.ingredient || ingredient.name || '';
      return name;
    }).join(' ');

    const searchUrl = `${app.searchUrl}${encodeURIComponent(searchQuery)}`;
    window.open(searchUrl, '_blank', 'noopener,noreferrer');
    
    return { 
      success: true, 
      method: 'search-fallback', 
      message: `Opened ${app.name} search page` 
    };
  }

  // Get cart status for an app
  async getCartStatus(appKey) {
    const app = this.apps[appKey];
    if (!app) {
      return { available: false, message: 'App not supported' };
    }

    return {
      available: true,
      hasApp: this.isMobileDevice(),
      hasWebCart: true,
      message: `${app.name} cart is available`
    };
  }

  // Get all available apps
  getAvailableApps() {
    return Object.keys(this.apps).map(key => ({
      key,
      ...this.apps[key]
    }));
  }
}

export default new GroceryCartService(); 