# 🚀 WeKno Food Delivery System

## Overview

The WeKno Food Delivery System is a comprehensive backend solution that integrates with TheMealDB API to fetch recipe ingredients and matches them with nearby grocery shops for ingredient delivery.

## 🎯 Features

- ✅ **Dynamic Ingredient Fetching**: Uses TheMealDB API to get real recipe ingredients
- ✅ **Shop Matching**: Matches ingredients with mock shop inventory
- ✅ **Distance Calculation**: Finds nearest shops using Haversine formula
- ✅ **Delivery Agent Assignment**: Automatically assigns nearest available delivery agent
- ✅ **Delivery Time Estimation**: Calculates realistic delivery times
- ✅ **Ingredient Coverage Analysis**: Shows available vs missing ingredients
- ✅ **Authentication**: JWT-based user authentication
- ✅ **Mock Google Distance Matrix**: Simulates real-world distance calculations

## 🏗️ System Architecture

```
User Request → Authentication → TheMealDB API → Shop Matching → Delivery Assignment → Response
     ↓              ↓              ↓              ↓              ↓              ↓
  Frontend    JWT Token    Recipe Data    Inventory    Agent Selection    Order Details
```

## 📡 API Endpoints

### 1. Create Delivery Order
**POST** `/delivery`

Creates a complete delivery order for recipe ingredients.

**Request Body:**
```json
{
  "dish_name": "Chicken Biryani",
  "servings": 2,
  "user_location": {
    "lat": 37.7749,
    "lng": -122.4194
  }
}
```

**Response:**
```json
{
  "success": true,
  "dish": "Chicken Biryani",
  "ingredients": [
    {
      "ingredient": "chicken",
      "quantity": 500,
      "unit": "g",
      "is_optional": false
    }
  ],
  "shop": {
    "name": "Fresh Mart",
    "distance_km": 1.2,
    "distance_text": "1.2 km",
    "duration_text": "4 mins",
    "location": {"lat": 37.7749, "lng": -122.4194},
    "available_ingredients": [...],
    "missing_ingredients": [...],
    "ingredient_coverage": "8/12 ingredients available"
  },
  "assigned_delivery_agent": {
    "id": "agent_001",
    "name": "Agent A",
    "status": "available"
  },
  "estimated_delivery_time": "25 mins",
  "order_details": {
    "order_id": "WK12345",
    "created_at": "2024-01-15T10:30:00Z",
    "user_id": 1,
    "servings": 2,
    "total_ingredients": 12,
    "available_ingredients_count": 8,
    "missing_ingredients_count": 4
  }
}
```

### 2. Get Available Shops
**GET** `/delivery/shops`

Returns all available shops with their inventory.

**Response:**
```json
{
  "success": true,
  "shops": [
    {
      "name": "Fresh Mart",
      "location": {"lat": 37.7749, "lng": -122.4194},
      "inventory_count": 45,
      "inventory": ["chicken", "rice", "onion", ...]
    }
  ],
  "total_shops": 5
}
```

### 3. Get Delivery Agents
**GET** `/delivery/agents`

Returns all delivery agents and their status.

**Response:**
```json
{
  "success": true,
  "agents": [
    {
      "id": "agent_001",
      "name": "Agent A",
      "status": "available",
      "current_location": {"lat": 37.7749, "lng": -122.4194}
    }
  ],
  "total_agents": 5,
  "available_agents": 4
}
```

### 4. Calculate Distance
**POST** `/delivery/calculate-distance`

Calculates distance between two points (for testing).

**Request Body:**
```json
{
  "origin": {"lat": 37.7749, "lng": -122.4194},
  "destination": {"lat": 37.7849, "lng": -122.4094}
}
```

**Response:**
```json
{
  "success": true,
  "distance_km": 1.2,
  "distance_matrix": {
    "distance": {"text": "1.2 km", "value": 1200},
    "duration": {"text": "4 mins", "value": 240}
  }
}
```

## 🏪 Mock Shop Data

The system includes 5 mock shops with different inventories:

1. **Fresh Mart** - General grocery items
2. **Super Foods** - Premium items + specialty ingredients
3. **Local Grocery** - Basic grocery items
4. **Asian Market** - Asian specialty ingredients
5. **Organic Corner** - Organic and health foods

Each shop has:
- Geographic coordinates (San Francisco area)
- Inventory list with 35-50 items
- Realistic ingredient matching

## 🚚 Delivery Agent System

5 mock delivery agents with:
- Unique IDs and names
- Current location tracking
- Availability status
- Automatic assignment based on proximity

## 📊 Ingredient Matching Logic

The system matches recipe ingredients with shop inventory using:

1. **Exact Match**: Direct string comparison
2. **Partial Match**: Checks if ingredient name contains shop item or vice versa
3. **Case Insensitive**: Converts to lowercase for comparison
4. **Fuzzy Matching**: Handles variations in ingredient names

## ⏰ Delivery Time Estimation

Delivery time is calculated based on:
- **Base Time**: 10 minutes for pickup
- **Travel Time**: 5 minutes per kilometer
- **Ingredient Time**: 2 minutes per ingredient
- **Minimum Time**: 15 minutes

## 🔧 Integration with Existing System

The delivery system integrates seamlessly with your existing:

- **TheMealDB Integration**: Uses existing `get_recipe_ingredients_from_themealdb()`
- **Authentication**: Uses existing JWT authentication
- **Ingredient Scaling**: Uses existing `scale_api_ingredients()`
- **Error Handling**: Consistent with existing error patterns

## 🧪 Testing

Run the test script to verify functionality:

```bash
cd backend
python test_delivery.py
```

This will test:
- ✅ Shop availability
- ✅ Delivery agent assignment
- ✅ Distance calculations
- ✅ Delivery orders for multiple dishes
- ✅ Different user locations

## 🚀 Usage Examples

### Frontend Integration

```javascript
// Create delivery order
const createDeliveryOrder = async (dishName, servings, userLocation) => {
  const response = await fetch('/delivery', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      dish_name: dishName,
      servings: servings,
      user_location: userLocation
    })
  });
  
  return response.json();
};

// Get available shops
const getShops = async () => {
  const response = await fetch('/delivery/shops');
  return response.json();
};

// Get delivery agents
const getAgents = async () => {
  const response = await fetch('/delivery/agents');
  return response.json();
};
```

### Backend Integration

```python
# The delivery system is already integrated into your existing app.py
# Just restart your Flask server to enable the new endpoints

# Test a delivery order
import requests

response = requests.post('http://localhost:5001/delivery', 
  json={
    'dish_name': 'Chicken Biryani',
    'servings': 2,
    'user_location': {'lat': 37.7749, 'lng': -122.4194}
  },
  headers={'Authorization': f'Bearer {token}'}
)

print(response.json())
```

## 🔄 Production Enhancements

For production deployment, consider:

1. **Real Google Maps API**: Replace mock distance calculations
2. **Database Integration**: Store shops, agents, and orders in database
3. **Real-time Tracking**: WebSocket integration for live delivery updates
4. **Payment Integration**: Stripe/PayPal for order payments
5. **Push Notifications**: Real-time order status updates
6. **Analytics**: Order tracking and business insights
7. **Multi-language Support**: Internationalization for global markets

## 📝 Environment Variables

Add these to your `.env` file for production:

```env
# Google Maps API (for real distance calculations)
GOOGLE_MAPS_API_KEY=your_google_maps_api_key

# Database (for storing orders)
DATABASE_URL=postgresql://user:password@localhost/weknow_db

# Redis (for real-time features)
REDIS_URL=redis://localhost:6379
```

## 🎉 Success!

Your WeKno food delivery system is now ready! The backend provides:

- ✅ Complete delivery order creation
- ✅ Real ingredient fetching from TheMealDB
- ✅ Smart shop matching and distance calculation
- ✅ Automatic delivery agent assignment
- ✅ Realistic delivery time estimation
- ✅ Comprehensive ingredient coverage analysis

**Next Steps:**
1. Test the endpoints using the provided test script
2. Integrate with your React frontend
3. Add real Google Maps API for production
4. Implement order tracking and notifications

Your food delivery app is now complete with professional-grade backend functionality! 🚀 