import React from 'react';

const VarietySelector = ({ varieties, onSelectVariety, onClose }) => {
  // Determine dish type and emoji based on first variety title
  const getDishTypeAndEmoji = () => {
    if (!varieties || varieties.length === 0) return { type: 'Dish', emoji: '🍽️' };
    
    const firstTitle = varieties[0].title.toLowerCase();
    
    if (firstTitle.includes('pizza')) return { type: 'Pizza', emoji: '🍕' };
    if (firstTitle.includes('sandwich')) return { type: 'Sandwich', emoji: '🥪' };
    if (firstTitle.includes('burger')) return { type: 'Burger', emoji: '🍔' };
    if (firstTitle.includes('pasta') || firstTitle.includes('spaghetti') || firstTitle.includes('fettuccine')) return { type: 'Pasta', emoji: '🍝' };
    if (firstTitle.includes('curry') || firstTitle.includes('masala') || firstTitle.includes('biryani')) return { type: 'Indian Cuisine', emoji: '🍛' };
    if (firstTitle.includes('salad')) return { type: 'Salad', emoji: '🥗' };
    if (firstTitle.includes('ice cream') || firstTitle.includes('cream')) return { type: 'Ice Cream', emoji: '🍦' };
    if (firstTitle.includes('cake')) return { type: 'Cake', emoji: '🍰' };
    if (firstTitle.includes('soup')) return { type: 'Soup', emoji: '🍲' };
    if (firstTitle.includes('steak')) return { type: 'Steak', emoji: '🥩' };
    if (firstTitle.includes('chicken')) return { type: 'Chicken', emoji: '🍗' };
    
    return { type: 'Dish', emoji: '🍽️' };
  };
  
  const { type, emoji } = getDishTypeAndEmoji();
  
  return (
    <div className="variety-selector-modal">
      <div className="variety-selector-content">
        <button className="close-button" onClick={onClose}>×</button>
        
        <div className="variety-selector">
          <h2>{emoji} Choose Your {type} Variety</h2>
          <p>Select from our delicious {type.toLowerCase()} options:</p>
          
          <div className="varieties-grid">
            {varieties.map((variety, index) => (
              <div 
                key={variety.id} 
                className="variety-card"
                onClick={() => onSelectVariety(variety)}
              >
                <div className="variety-image">
                  <img 
                    src={variety.image || 'https://images.pexels.com/photos/825661/pexels-photo-825661.jpeg?w=200&h=150&fit=crop&crop=center'} 
                    alt={variety.title}
                    onError={(e) => {
                      e.target.style.display = 'none';
                      e.target.nextSibling.style.display = 'block';
                    }}
                  />
                  <div className="fallback-image">
                    {emoji} {type} Image
                  </div>
                </div>
                <div className="variety-info">
                  <h3>{variety.title}</h3>
                  <p className="variety-servings">Serves {variety.servings} people</p>
                  <div className="variety-confidence">
                    <span className="confidence-badge">
                      {Math.round(variety.confidence * 100)}% Match
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
          
          <div className="variety-actions">
            <button className="cancel-button" onClick={onClose}>
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VarietySelector; 