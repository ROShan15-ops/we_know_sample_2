import React, { useState } from 'react';
import { GroceryOrderButton } from './index.jsx';

const DishWithGroceryOrder = () => {
  const [selectedDish, setSelectedDish] = useState(null);
  const [ingredients, setIngredients] = useState([]);

  // Example dishes with ingredients (this would come from your API)
  const sampleDishes = [
    {
      id: 1,
      name: 'Paneer Butter Masala',
      ingredients: [
        { ingredient: 'Paneer', quantity: 200, unit: 'grams' },
        { ingredient: 'Butter', quantity: 50, unit: 'grams' },
        { ingredient: 'Tomatoes', quantity: 4, unit: 'pieces' },
        { ingredient: 'Onions', quantity: 2, unit: 'pieces' },
        { ingredient: 'Ginger', quantity: 1, unit: 'inch' },
        { ingredient: 'Garlic', quantity: 6, unit: 'cloves' },
        { ingredient: 'Cream', quantity: 100, unit: 'ml' },
        { ingredient: 'Spices', quantity: 1, unit: 'tablespoon' }
      ]
    },
    {
      id: 2,
      name: 'Chicken Tikka Masala',
      ingredients: [
        { ingredient: 'Chicken', quantity: 500, unit: 'grams' },
        { ingredient: 'Yogurt', quantity: 200, unit: 'ml' },
        { ingredient: 'Tomatoes', quantity: 3, unit: 'pieces' },
        { ingredient: 'Onions', quantity: 2, unit: 'pieces' },
        { ingredient: 'Ginger', quantity: 1, unit: 'inch' },
        { ingredient: 'Garlic', quantity: 4, unit: 'cloves' },
        { ingredient: 'Cream', quantity: 150, unit: 'ml' },
        { ingredient: 'Garam Masala', quantity: 1, unit: 'teaspoon' }
      ]
    },
    {
      id: 3,
      name: 'Margherita Pizza',
      ingredients: [
        { ingredient: 'Pizza Dough', quantity: 1, unit: 'piece' },
        { ingredient: 'Mozzarella Cheese', quantity: 200, unit: 'grams' },
        { ingredient: 'Tomato Sauce', quantity: 150, unit: 'ml' },
        { ingredient: 'Fresh Basil', quantity: 20, unit: 'grams' },
        { ingredient: 'Olive Oil', quantity: 30, unit: 'ml' }
      ]
    }
  ];

  const handleDishSelect = (dish) => {
    setSelectedDish(dish);
    setIngredients(dish.ingredients);
  };

  return (
    <div className="dish-grocery-demo">
      <div className="demo-header">
        <h2>🍽️ Dish Selection with Grocery Ordering</h2>
        <p>Select a dish to see ingredients and order them from grocery apps</p>
      </div>

      <div className="dishes-grid">
        {sampleDishes.map((dish) => (
          <div 
            key={dish.id} 
            className={`dish-card ${selectedDish?.id === dish.id ? 'selected' : ''}`}
            onClick={() => handleDishSelect(dish)}
          >
            <h3>{dish.name}</h3>
            <p>{dish.ingredients.length} ingredients</p>
            <div className="dish-ingredients-preview">
              {dish.ingredients.slice(0, 3).map((ingredient, index) => (
                <span key={index} className="ingredient-preview">
                  {ingredient.ingredient}
                </span>
              ))}
              {dish.ingredients.length > 3 && (
                <span className="ingredient-preview">+{dish.ingredients.length - 3} more</span>
              )}
            </div>
          </div>
        ))}
      </div>

      {selectedDish && (
        <div className="selected-dish-section">
          <div className="dish-info">
            <h3>Selected Dish: {selectedDish.name}</h3>
            <p>Ingredients needed for this recipe:</p>
          </div>
          
          <GroceryOrderButton 
            ingredients={ingredients}
            dishName={selectedDish.name}
          />
        </div>
      )}
    </div>
  );
};

export default DishWithGroceryOrder; 