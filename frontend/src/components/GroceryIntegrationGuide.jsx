import React from 'react';

const GroceryIntegrationGuide = () => {
  return (
    <div className="integration-guide">
      <div className="guide-header">
        <h2>🛒 Grocery Order Integration Guide</h2>
        <p>How to integrate grocery ordering into your existing dish selection system</p>
      </div>

      <div className="guide-sections">
        <div className="guide-section">
          <h3>1. Basic Integration</h3>
          <p>Add the GroceryOrderButton component to your existing dish display:</p>
          <pre className="code-block">
{`import { GroceryOrderButton } from './components/index.jsx';

// In your component where you show dish details
{selectedDish && (
  <div className="dish-details">
    <h3>{selectedDish.name}</h3>
    <p>Ingredients: {selectedDish.ingredients.length}</p>
    
    {/* Add this line to show grocery ordering */}
    <GroceryOrderButton 
      ingredients={selectedDish.ingredients}
      dishName={selectedDish.name}
    />
  </div>
)}`}
          </pre>
        </div>

        <div className="guide-section">
          <h3>2. Ingredient Format Support</h3>
          <p>The component supports multiple ingredient formats:</p>
          <pre className="code-block">
{`// String array format
ingredients={['Paneer', 'Butter', 'Tomatoes']}

// Object array format (from your API)
ingredients={[
  { ingredient: 'Paneer', quantity: 200, unit: 'grams' },
  { ingredient: 'Butter', quantity: 50, unit: 'grams' }
]}

// Mixed format
ingredients={[
  'Paneer',
  { ingredient: 'Butter', quantity: 50, unit: 'grams' },
  'Tomatoes'
]}`}
          </pre>
        </div>

        <div className="guide-section">
          <h3>3. Supported Grocery Apps</h3>
          <div className="apps-list">
            <div className="app-item">
              <span className="app-icon">🛒</span>
              <div>
                <strong>Blinkit</strong>
                <p>URL: https://www.blinkit.com/search?q=</p>
              </div>
            </div>
            <div className="app-item">
              <span className="app-icon">⚡</span>
              <div>
                <strong>Zepto</strong>
                <p>URL: https://www.zepto.in/search?q=</p>
              </div>
            </div>
            <div className="app-item">
              <span className="app-icon">🛍️</span>
              <div>
                <strong>BigBasket</strong>
                <p>URL: https://www.bigbasket.com/ps/?q=</p>
              </div>
            </div>
          </div>
        </div>

        <div className="guide-section">
          <h3>4. Adding More Grocery Apps</h3>
          <p>To add more grocery apps, modify the groceryApps object in GroceryOrderButton.jsx:</p>
          <pre className="code-block">
{`const groceryApps = {
  blinkit: {
    name: 'Blinkit',
    baseUrl: 'https://www.blinkit.com/search?q=',
    icon: '🛒',
    color: '#ff6b35'
  },
  zepto: {
    name: 'Zepto',
    baseUrl: 'https://www.zepto.in/search?q=',
    icon: '⚡',
    color: '#00b894'
  },
  bigbasket: {
    name: 'BigBasket',
    baseUrl: 'https://www.bigbasket.com/ps/?q=',
    icon: '🛍️',
    color: '#0984e3'
  },
  // Add new apps here
  newapp: {
    name: 'New App',
    baseUrl: 'https://newapp.com/search?q=',
    icon: '🆕',
    color: '#your-color'
  }
};`}
          </pre>
        </div>

        <div className="guide-section">
          <h3>5. Error Handling</h3>
          <p>The component includes built-in error handling:</p>
          <ul>
            <li>✅ Handles empty ingredients arrays</li>
            <li>✅ Handles null/undefined ingredients</li>
            <li>✅ Cleans ingredient names (removes quantities, units)</li>
            <li>✅ Shows fallback message when no ingredients available</li>
            <li>✅ Validates search query before opening URLs</li>
          </ul>
        </div>

        <div className="guide-section">
          <h3>6. Example Integration with Your Current System</h3>
          <p>Here's how to integrate with your existing MainApp component:</p>
          <pre className="code-block">
{`// In your MainApp.jsx or wherever you show dish results
{recipeInfo && ingredients && (
  <div className="results">
    <div className="recipe-info">
      <h2>{recipeInfo.title}</h2>
      <p>Dish Type: {recipeInfo.dish_type}</p>
      <p>Confidence: {recipeInfo.confidence}</p>
    </div>
    
    <div className="ingredients-list">
      <h3>Ingredients:</h3>
      <ul>
        {ingredients.map((ingredient, index) => (
          <li key={index} className="ingredient-item">
            <span className="ingredient-amount">
              {ingredient.quantity} {ingredient.unit}
            </span>
            <span className="ingredient-name">{ingredient.ingredient}</span>
          </li>
        ))}
      </ul>
    </div>
    
    {/* Add grocery ordering here */}
    <GroceryOrderButton 
      ingredients={ingredients}
      dishName={recipeInfo.title}
    />
    
    <div className="action-buttons">
      {/* Your existing buttons */}
    </div>
  </div>
)}`}
          </pre>
        </div>
      </div>
    </div>
  );
};

export default GroceryIntegrationGuide; 