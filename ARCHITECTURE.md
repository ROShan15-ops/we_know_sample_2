# WeKno Food Delivery App - System Architecture

## 🏗️ **System Overview**

WeKno is a full-stack food delivery application that connects users with recipe ingredients and grocery delivery services. The system uses a microservices-inspired architecture with separate frontend and backend components.

## 📊 **Architecture Diagram**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CLIENT LAYER                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  React Frontend (Port 3000)                                              │
│  ├── User Interface Components                                            │
│  ├── State Management (useState, useEffect)                              │
│  ├── API Integration (fetch)                                             │
│  └── External Service Integration                                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTP/REST API
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        API GATEWAY LAYER                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  Flask Backend (Port 5001)                                               │
│  ├── Authentication Service (JWT)                                        │
│  ├── Ingredient Service (Spoonacular API)                               │
│  ├── Delivery Service (Mock Location)                                   │
│  ├── Cart Service (Mock Grocery Apps)                                   │
│  └── CORS Configuration                                                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ External APIs
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        EXTERNAL SERVICES LAYER                            │
├─────────────────────────────────────────────────────────────────────────────┤
│  Spoonacular API (Recipe Data)                                           │
│  Grocery Delivery Apps (Mocked)                                          │
│  ├── BigBasket                                                           │
│  ├── Blinkit                                                             │
│  └── Zepto                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 🏛️ **Detailed Architecture**

### **1. Frontend Architecture (React)**

```
frontend/src/
├── components/
│   ├── MainApp.jsx              # Main application container
│   ├── LoginModal.jsx           # User authentication
│   ├── SignupModal.jsx          # User registration
│   ├── LandingPage.jsx          # Welcome page
│   ├── Orders.jsx               # Order management
│   ├── DeliveryTracker.jsx      # Order tracking
│   ├── VarietySelector.jsx      # Dish variety selection
│   └── DeliveryDashboard.jsx    # Delivery tracking
├── App.css                      # Global styles
└── index.jsx                    # Application entry point
```

#### **Frontend Features:**
- **Component-Based Architecture**: Modular React components
- **State Management**: React hooks (useState, useEffect, useCallback)
- **API Integration**: Fetch API for backend communication
- **External Integration**: Direct integration with delivery services
- **Responsive Design**: Mobile-first CSS approach

### **2. Backend Architecture (Flask)**

```
backend/
├── app.py                       # Main Flask application
├── config.py                    # Configuration management
├── models.py                    # Database models
├── auth_service.py              # Authentication logic
├── ingredient_service.py        # Recipe & ingredient processing
├── delivery_service.py          # Delivery & location services

└── mock_data.py                 # Mock data for testing
```

#### **Backend Services:**

##### **A. Authentication Service (`auth_service.py`)**
```python
# JWT-based authentication
- create_access_token()     # Generate JWT tokens
- verify_token()           # Validate JWT tokens
- create_user()           # User registration
- authenticate_user()      # User login
```

##### **B. Ingredient Service (`ingredient_service.py`)**
```python
# Recipe and ingredient processing
- get_recipe_ingredients_from_spoonacular()  # Primary API
- extract_dish_type()                        # NLP processing
- validate_recipe_relevance()                # Recipe validation
- scale_api_ingredients()                    # Serving size scaling
```

##### **C. Delivery Service (`delivery_service.py`)**
```python
# Delivery and location services
- find_and_rank_shops()           # Shop matching algorithm
- assign_delivery_agent()         # Agent assignment
- estimate_delivery_time()        # Time estimation
- get_google_distance_matrix()    # Distance calculation (mocked)
```



### **3. API Endpoints Architecture**

#### **Authentication Endpoints:**
```
POST /auth/register              # User registration
POST /auth/login                 # User login
GET  /auth/me                   # Get user profile
```

#### **Recipe & Ingredient Endpoints:**
```
POST /ingredients               # Get recipe ingredients
POST /search-varieties          # Search dish varieties
```

#### **Delivery Endpoints:**
```
POST /delivery                  # Create delivery order
POST /delivery/test             # Test delivery (no auth)
GET  /delivery/shops            # Get available shops
GET  /delivery/agents           # Get delivery agents
POST /delivery/ranked-shops     # Get ranked shops
```



### **4. Data Flow Architecture**

#### **A. Recipe Ingredient Flow:**
```
1. User Input (Dish Name)
   ↓
2. NLP Processing (TextBlob)
   ├── extract_dish_type()
   ├── clean_dish_name()
   └── validate_recipe_relevance()
   ↓
3. Spoonacular API Call
   ├── Recipe search
   ├── Ingredient extraction
   └── Quantity/unit parsing
   ↓
4. Ingredient Processing
   ├── Scaling for servings
   ├── Cleaning and formatting
   └── Validation
   ↓
5. Response to Frontend
```

#### **B. Delivery Order Flow:**
```
1. Ingredient Fetching
   ↓
2. Shop Matching Algorithm
   ├── Distance calculation
   ├── Ingredient availability check
   └── Match percentage calculation
   ↓
3. Shop Ranking
   ├── Sort by match percentage
   ├── Sort by distance
   └── Filter by minimum requirements
   ↓
4. Delivery Agent Assignment
   ├── Find nearest agent
   ├── Check availability
   └── Assign to order
   ↓
5. Order Creation
   ├── Generate order ID
   ├── Calculate delivery time
   └── Return order details
```

#### **C. Grocery Integration Flow:**
```
1. Ingredient List
   ↓
2. Search Query Generation
   ├── Clean ingredient names
   ├── Convert to generic terms
   └── Create multiple queries
   ↓
3. Multi-Method Integration
   ├── Auto Cart Addition (mocked)
   ├── Deep Link Opening
   ├── Web Search Tabs
   └── Fallback Search
   ↓
4. User Experience
   ├── Multiple tab opening
   ├── Success notifications
   └── Error handling
```

### **5. Database Architecture**

#### **SQLite Database Schema:**
```sql
-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table (for future expansion)
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    order_id TEXT UNIQUE,
    dish_name TEXT,
    ingredients TEXT,
    shop_name TEXT,
    delivery_agent TEXT,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

### **6. Security Architecture**

#### **Authentication & Authorization:**
- **JWT Tokens**: Stateless authentication
- **Password Hashing**: Secure password storage
- **CORS Configuration**: Cross-origin request handling
- **Input Validation**: Request data sanitization

#### **API Security:**
- **Rate Limiting**: Request throttling (future)
- **Error Handling**: Secure error messages
- **Input Sanitization**: XSS prevention
- **HTTPS**: Secure communication (production)

### **7. External Service Integration**

#### **A. Spoonacular API Integration:**
```python
# Real-time recipe data
- Base URL: https://api.spoonacular.com/recipes
- Endpoints: /complexSearch, /information
- Authentication: API Key
- Rate Limits: 150 requests/day (free tier)
```

#### **B. Grocery App Integration:**
```javascript
// Mocked external services
- BigBasket: https://www.bigbasket.com/
- Blinkit: https://blinkit.com/
- Zepto: https://www.zepto.in/
- Integration: Deep links + Web search
```

### **8. Performance Architecture**

#### **Frontend Performance:**
- **Component Optimization**: React.memo, useCallback
- **Lazy Loading**: Code splitting for components
- **Caching**: Browser caching for static assets
- **Bundle Optimization**: Webpack optimization

#### **Backend Performance:**
- **Database Optimization**: Indexed queries
- **API Caching**: Response caching (future)
- **Connection Pooling**: Database connection management
- **Async Processing**: Background task processing (future)

### **9. Scalability Architecture**

#### **Horizontal Scaling:**
```
Load Balancer
    ├── Backend Server 1 (Flask)
    ├── Backend Server 2 (Flask)
    └── Backend Server N (Flask)
```

#### **Database Scaling:**
- **Read Replicas**: Multiple database instances
- **Sharding**: Data partitioning (future)
- **Caching Layer**: Redis integration (future)

### **10. Deployment Architecture**

#### **Development Environment:**
```
Frontend: http://localhost:3000 (React Dev Server)
Backend:  http://localhost:5001 (Flask Development)
Database: SQLite (local file)
```

#### **Production Environment (Future):**
```
Frontend: CDN + Static Hosting
Backend:  Cloud Platform (AWS/GCP/Azure)
Database: Managed SQL Database
Caching:  Redis Cluster
Monitoring: Application Performance Monitoring
```

### **11. Error Handling Architecture**

#### **Frontend Error Handling:**
```javascript
// Try-catch blocks for API calls
// User-friendly error messages
// Fallback UI components
// Network error recovery
```

#### **Backend Error Handling:**
```python
# Global exception handlers
# Structured error responses
# Logging and monitoring
# Graceful degradation
```

### **12. Testing Architecture**

#### **Frontend Testing:**
- **Unit Tests**: Component testing
- **Integration Tests**: API integration
- **E2E Tests**: User workflow testing

#### **Backend Testing:**
- **Unit Tests**: Service function testing
- **Integration Tests**: API endpoint testing
- **Mock Testing**: External service mocking

## 🎯 **Key Architectural Decisions**

### **1. Microservices-Inspired Design**
- **Separation of Concerns**: Each service has a specific responsibility
- **Independent Deployment**: Services can be deployed separately
- **Technology Flexibility**: Different services can use different technologies

### **2. API-First Architecture**
- **RESTful Design**: Standard HTTP methods and status codes
- **JSON Communication**: Lightweight data exchange
- **Stateless Design**: No server-side session storage

### **3. Component-Based Frontend**
- **Reusable Components**: Modular UI building blocks
- **State Management**: Centralized state with React hooks
- **Responsive Design**: Mobile-first approach

### **4. Mocked External Services**
- **Development Flexibility**: No dependency on external APIs
- **Testing Capability**: Controlled testing environment
- **Cost Efficiency**: No external API costs during development

## 📈 **Architecture Benefits**

1. **Scalability**: Easy to scale individual components
2. **Maintainability**: Clear separation of concerns
3. **Testability**: Isolated components for testing
4. **Flexibility**: Easy to modify or replace components
5. **Performance**: Optimized for specific use cases
6. **Security**: Layered security approach
7. **Reliability**: Graceful error handling and fallbacks

## 🔮 **Future Architecture Enhancements**

1. **Message Queue**: Redis/RabbitMQ for async processing
2. **Caching Layer**: Redis for performance optimization
3. **Monitoring**: APM and logging solutions
4. **CI/CD**: Automated deployment pipelines
5. **Containerization**: Docker containerization
6. **Microservices**: Full microservices architecture
7. **Event-Driven**: Event sourcing and CQRS patterns

---

**Architecture Summary**: WeKno uses a modern, scalable architecture with clear separation between frontend and backend services, comprehensive API integration, and robust error handling for a reliable food delivery experience. 