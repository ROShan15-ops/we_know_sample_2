# Data Sources & APIs Documentation - WeKno Food Delivery App

## 📊 Primary Data Sources

### 1. Spoonacular API
- **API Key**: `9a62ed1cf32144f2aa56665587b0836c` (Provided by user)
- **Base URL**: `https://api.spoonacular.com/`
- **Documentation**: https://spoonacular.com/food-api/docs
- **Usage in Project**: 
  - Recipe search and ingredient extraction
  - Primary source for dish ingredients
  - Used in `backend/ingredient_service.py`
- **Endpoints Used**:
  - `/recipes/complexSearch` - Search for recipes
  - `/recipes/{id}/information` - Get recipe details with ingredients



## 🛒 Grocery Delivery APIs (Mocked)



## 🗺️ Location & Distance APIs

### 6. Google Distance Matrix API (Mocked)
- **Base URL**: `https://maps.googleapis.com/maps/api/distancematrix/json`
- **Documentation**: https://developers.google.com/maps/documentation/distance-matrix
- **Usage in Project**: 
  - Calculate delivery distances
  - Used in `backend/delivery_service.py`
  - Mocked implementation for demonstration

## 📦 Mock Data Sources

### 7. Shop Data (Mocked)
- **Location**: `backend/mock_data.py`
- **Data Type**: Grocery store locations and inventory
- **Usage**: Delivery service shop matching

### 8. Delivery Agents Data (Mocked)
- **Location**: `backend/mock_data.py`
- **Data Type**: Delivery personnel information
- **Usage**: Delivery assignment system

### 9. Product Database (Mocked)
- **Location**: `frontend/src/components/AutoCartService.js`
- **Data Type**: Grocery product information
- **Usage**: Product matching for cart addition

## 🔧 Development Tools & Libraries

### 10. TextBlob (NLP Processing)
- **Documentation**: https://textblob.readthedocs.io/
- **Usage in Project**: 
  - Natural language processing for dish names
  - Used in `backend/ingredient_service.py`
- **Installation**: `pip install textblob`

### 11. Flask (Backend Framework)
- **Documentation**: https://flask.palletsprojects.com/
- **Usage in Project**: 
  - REST API server
  - Main backend framework
- **Installation**: `pip install flask`

### 12. React (Frontend Framework)
- **Documentation**: https://reactjs.org/
- **Usage in Project**: 
  - User interface components
  - State management
- **Installation**: `npm install react`

## 📋 API Integration Details

### Spoonacular API Integration
```python
# backend/ingredient_service.py
def get_recipe_ingredients_from_spoonacular(dish_name, servings=2):
    url = f"https://api.spoonacular.com/recipes/complexSearch"
    params = {
        'apiKey': SPOONACULAR_API_KEY,
        'query': dish_name,
        'number': 1,
        'addRecipeInformation': True
    }
```



### Grocery App Integration
```javascript
// frontend/src/components/RealGroceryCartService.js
const searchUrls = {
  'BigBasket': 'https://www.bigbasket.com/ps/?q=',
  'Blinkit': 'https://blinkit.com/search?q=',
  'Zepto': 'https://www.zepto.in/search?q='
};
```

## 🔐 Authentication & Security

### JWT Authentication (Mocked)
- **Implementation**: Custom JWT token system
- **Location**: `backend/auth_service.py`
- **Usage**: User login and session management

### CORS Configuration
- **Implementation**: Cross-origin resource sharing
- **Location**: `backend/app.py`
- **Usage**: Allow frontend-backend communication

## 📊 Data Flow Architecture

```
User Input (Dish Name)
    ↓
Spoonacular API (Primary)
    ↓
Ingredient Processing (NLP)
    ↓
Grocery App Integration
    ↓
Search Query Generation
    ↓
Tab Opening (Multiple Apps)
```

## 🔗 External Service Links

### Recipe & Ingredient APIs
1. **Spoonacular**: https://spoonacular.com/food-api



### Development Tools
1. **Flask**: https://flask.palletsprojects.com/
2. **React**: https://reactjs.org/
3. **TextBlob**: https://textblob.readthedocs.io/

## 📝 API Response Examples

### Spoonacular API Response
```json
{
  "results": [
    {
      "id": 12345,
      "title": "Roasted Peppers, Spinach & Feta Pizza",
      "extendedIngredients": [
        {
          "id": 1009,
          "name": "feta cheese",
          "amount": 0.5,
          "unit": "cup"
        }
      ]
    }
  ]
}
```



## 🚀 Deployment Information

### Backend Server
- **URL**: `http://localhost:5001`
- **Health Check**: `http://localhost:5001/health`
- **Framework**: Flask (Python)

### Frontend Server
- **URL**: `http://localhost:3000`
- **Framework**: React (JavaScript)

## 📋 Summary

This project integrates multiple data sources:
- **1 Real API**: Spoonacular (primary recipe data)
- **1 Mocked API**: Google Distance Matrix (location services)
- **Multiple Libraries**: TextBlob, Flask, React
- **Custom Mock Data**: Shop inventory, delivery agents

All external APIs are properly documented and integrated with error handling mechanisms. 