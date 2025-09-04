import React from 'react';
import logo from '../assets/logo.svg';

const LandingPage = ({ onLoginClick, onSignupClick, navigateToHome }) => {
  const popularCuisines = [
    { 
      name: 'Italian', 
      icon: '🍝', 
      description: 'Pasta, Pizza, Risotto',
      country: 'Italy',
      flagColors: ['#009246', '#ffffff', '#ce2b37'],
      flagEmoji: '🇮🇹',
      dishes: [
        { name: 'Margherita Pizza', image: 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=200&h=150&fit=crop&crop=center' },
        { name: 'Spaghetti Carbonara', image: 'https://images.unsplash.com/photo-1621996346565-e3dbc353d2e5?w=200&h=150&fit=crop&crop=center' },
        { name: 'Risotto ai Funghi', image: 'https://images.unsplash.com/photo-1476124369491-e7addf5db371?w=200&h=150&fit=crop&crop=center' }
      ]
    },
    { 
      name: 'Mexican', 
      icon: '🌮', 
      description: 'Tacos, Enchiladas, Guacamole',
      country: 'Mexico',
      flagColors: ['#006847', '#ffffff', '#ce1126'],
      flagEmoji: '🇲🇽',
      dishes: [
        { name: 'Street Tacos', image: 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=200&h=150&fit=crop&crop=center' },
        { name: 'Chicken Enchiladas', image: 'https://images.unsplash.com/photo-1582169296194-e4d644c48063?w=200&h=150&fit=crop&crop=center' },
        { name: 'Fresh Guacamole', image: 'https://images.unsplash.com/photo-1541519227354-08fa5d50c44d?w=200&h=150&fit=crop&crop=center' }
      ]
    },
    { 
      name: 'Indian', 
      icon: '🍛', 
      description: 'Curry, Biryani, Naan',
      country: 'India',
      flagColors: ['#ff9933', '#ffffff', '#138808'],
      flagEmoji: '🇮🇳',
      dishes: [
        { name: 'Butter Chicken', image: 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=200&h=150&fit=crop&crop=center' },
        { name: 'Chicken Biryani', image: 'https://images.unsplash.com/photo-1633945274405-b6c8069047b0?w=200&h=150&fit=crop&crop=center' },
        { name: 'Garlic Naan', image: 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=200&h=150&fit=crop&crop=center' }
      ]
    },
    { 
      name: 'Chinese', 
      icon: '🥢', 
      description: 'Dumplings, Stir-fry, Noodles',
      country: 'China',
      flagColors: ['#de2910', '#ffde00'],
      flagEmoji: '🇨🇳',
      dishes: [
        { name: 'Steamed Dumplings', image: 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=200&h=150&fit=crop&crop=center' },
        { name: 'Kung Pao Chicken', image: 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=200&h=150&fit=crop&crop=center' },
        { name: 'Beef Noodles', image: 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=200&h=150&fit=crop&crop=center' }
      ]
    },
    { 
      name: 'Japanese', 
      icon: '🍱', 
      description: 'Sushi, Ramen, Tempura',
      country: 'Japan',
      flagColors: ['#ffffff', '#bc002d'],
      flagEmoji: '🇯🇵',
      dishes: [
        { name: 'Fresh Sushi', image: 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=200&h=150&fit=crop&crop=center' },
        { name: 'Tonkotsu Ramen', image: 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=200&h=150&fit=crop&crop=center' },
        { name: 'Tempura Shrimp', image: 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=200&h=150&fit=crop&crop=center' }
      ]
    },
    { 
      name: 'Thai', 
      icon: '🍜', 
      description: 'Pad Thai, Tom Yum, Green Curry',
      country: 'Thailand',
      flagColors: ['#a51931', '#ffffff', '#2d2a4a'],
      flagEmoji: '🇹🇭',
      dishes: [
        { name: 'Pad Thai', image: 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=200&h=150&fit=crop&crop=center' },
        { name: 'Tom Yum Soup', image: 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=200&h=150&fit=crop&crop=center' },
        { name: 'Green Curry', image: 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=200&h=150&fit=crop&crop=center' }
      ]
    },
    { 
      name: 'Mediterranean', 
      icon: '🥙', 
      description: 'Hummus, Falafel, Greek Salad',
      country: 'Greece',
      flagColors: ['#0d5eaf', '#ffffff'],
      flagEmoji: '🇬🇷',
      dishes: [
        { name: 'Fresh Hummus', image: 'https://images.unsplash.com/photo-1541519227354-08fa5d50c44d?w=200&h=150&fit=crop&crop=center' },
        { name: 'Crispy Falafel', image: 'https://images.unsplash.com/photo-1582169296194-e4d644c48063?w=200&h=150&fit=crop&crop=center' },
        { name: 'Greek Salad', image: 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=200&h=150&fit=crop&crop=center' }
      ]
    },
    { 
      name: 'American', 
      icon: '🍔', 
      description: 'Burgers, BBQ, Apple Pie',
      country: 'USA',
      flagColors: ['#b22234', '#ffffff', '#3c3b6e'],
      flagEmoji: '🇺🇸',
      dishes: [
        { name: 'Classic Burger', image: 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=200&h=150&fit=crop&crop=center' },
        { name: 'BBQ Ribs', image: 'https://images.unsplash.com/photo-1544025162-d76694265947?w=200&h=150&fit=crop&crop=center' },
        { name: 'Apple Pie', image: 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=200&h=150&fit=crop&crop=center' }
      ]
    },
    { 
      name: 'French', 
      icon: '🥐', 
      description: 'Croissants, Coq au Vin, Ratatouille',
      country: 'France',
      flagColors: ['#002395', '#ffffff', '#ed2939'],
      flagEmoji: '🇫🇷',
      dishes: [
        { name: 'Butter Croissant', image: 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=200&h=150&fit=crop&crop=center' },
        { name: 'Coq au Vin', image: 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=200&h=150&fit=crop&crop=center' },
        { name: 'Ratatouille', image: 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=200&h=150&fit=crop&crop=center' }
      ]
    },
    { 
      name: 'Spanish', 
      icon: '🥘', 
      description: 'Paella, Tapas, Gazpacho',
      country: 'Spain',
      flagColors: ['#aa151b', '#f1bf00'],
      flagEmoji: '🇪🇸',
      dishes: [
        { name: 'Seafood Paella', image: 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=200&h=150&fit=crop&crop=center' },
        { name: 'Spanish Tapas', image: 'https://images.unsplash.com/photo-1582169296194-e4d644c48063?w=200&h=150&fit=crop&crop=center' },
        { name: 'Gazpacho Soup', image: 'https://images.unsplash.com/photo-1541519227354-08fa5d50c44d?w=200&h=150&fit=crop&crop=center' }
      ]
    },
    { 
      name: 'Korean', 
      icon: '🍲', 
      description: 'Bibimbap, Kimchi, Bulgogi',
      country: 'South Korea',
      flagColors: ['#cd2e3a', '#ffffff', '#0047a0'],
      flagEmoji: '🇰🇷',
      dishes: [
        { name: 'Bibimbap Bowl', image: 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=200&h=150&fit=crop&crop=center' },
        { name: 'Kimchi Fried Rice', image: 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=200&h=150&fit=crop&crop=center' },
        { name: 'Bulgogi Beef', image: 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=200&h=150&fit=crop&crop=center' }
      ]
    },
    { 
      name: 'Vietnamese', 
      icon: '🍜', 
      description: 'Pho, Banh Mi, Spring Rolls',
      country: 'Vietnam',
      flagColors: ['#da251d', '#ffff00'],
      flagEmoji: '🇻🇳',
      dishes: [
        { name: 'Beef Pho', image: 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=200&h=150&fit=crop&crop=center' },
        { name: 'Banh Mi Sandwich', image: 'https://images.unsplash.com/photo-1582169296194-e4d644c48063?w=200&h=150&fit=crop&crop=center' },
        { name: 'Fresh Spring Rolls', image: 'https://images.unsplash.com/photo-1541519227354-08fa5d50c44d?w=200&h=150&fit=crop&crop=center' }
      ]
    },

  ];

  return (
    <div className="App">
      {/* Header */}
      <header className="App-header">
        <div className="header-main">
          <div className="header-content">
            <div className="logo" onClick={() => {
              navigateToHome();
              window.scrollTo({ top: 0, behavior: 'smooth' });
            }} style={{ cursor: 'pointer' }}>
              <img src={logo} alt="We Know Logo" className="landing-logo" />
            </div>
            <nav className="nav-links">
              <a href="#home" className="nav-link">
                <span className="nav-icon">🏠</span>
                <span>Home</span>
              </a>
              <a href="#delivery" className="nav-link">
                <span className="nav-icon">🚚</span>
                <span>Delivery</span>
              </a>
              <a href="#about-us" className="nav-link" onClick={(e) => {
                e.preventDefault();
                document.getElementById('about-us-section').scrollIntoView({ behavior: 'smooth' });
              }}>
                <span className="nav-icon">ℹ️</span>
                <span>About Us</span>
              </a>
            </nav>
            <div className="auth-buttons">
              <button className="login-btn" onClick={onLoginClick}>LOGIN</button>
              <button className="signup-btn" onClick={onSignupClick}>SIGN UP</button>
          </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-overlay"></div>
        <div className="hero-content">
          <h1 className="hero-title">Discover Amazing Recipes</h1>
          <p className="hero-subtitle">You know your dish, we know your ingredients</p>
          <p className="hero-description">Get instant grocery lists for any recipe with our AI-powered ingredient finder</p>
      </div>
      </section>

      {/* Moving Offers Banner */}
      <section className="offers-banner">
        <div className="offers-container">
          <div className="offers-scroll">
            <div className="offer-item">
              <span className="offer-icon">🎉</span>
              <span className="offer-text">🔥 FLASH SALE: 50% OFF on Premium Ingredients!</span>
            </div>
            <div className="offer-item">
              <span className="offer-icon">🚚</span>
              <span className="offer-text">⚡ FREE Express Delivery on Orders Above $75</span>
            </div>
            <div className="offer-item">
              <span className="offer-icon">⭐</span>
              <span className="offer-text">🎁 New Users: 25% OFF + Free Welcome Kit</span>
            </div>
            <div className="offer-item">
              <span className="offer-icon">🔥</span>
              <span className="offer-text">🌶️ Spicy Deal: 40% OFF on Asian Ingredients</span>
            </div>
            <div className="offer-item">
              <span className="offer-icon">🎁</span>
              <span className="offer-text">💝 Buy 3 Get 2 FREE on Organic Products</span>
            </div>
            <div className="offer-item">
              <span className="offer-icon">⚡</span>
              <span className="offer-text">🚀 1-Hour Delivery Available in Select Areas</span>
            </div>
            <div className="offer-item">
              <span className="offer-icon">🏆</span>
              <span className="offer-text">👑 VIP Members: 30% OFF + Priority Support</span>
            </div>
            <div className="offer-item">
              <span className="offer-icon">🌿</span>
              <span className="offer-text">🌱 Plant-Based: 35% OFF on Vegan Ingredients</span>
            </div>
            <div className="offer-item">
              <span className="offer-icon">🍕</span>
              <span className="offer-text">🍕 Pizza Night: 45% OFF on Italian Essentials</span>
            </div>
            <div className="offer-item">
              <span className="offer-icon">🎯</span>
              <span className="offer-text">🎯 Loyalty Rewards: Earn Points on Every Order</span>
            </div>
          </div>
        </div>
      </section>

      {/* Food Categories Section */}
      <section className="categories-section">
        <div className="categories-content">
          <h2 className="section-title">Popular Cuisines</h2>
          <div className="categories-grid">
          {popularCuisines.map((cuisine, index) => (
              <div key={index} className="category-card" style={{
                background: `linear-gradient(135deg, ${cuisine.flagColors[0]} 0%, ${cuisine.flagColors[1] || cuisine.flagColors[0]} 50%, ${cuisine.flagColors[2] || cuisine.flagColors[1] || cuisine.flagColors[0]} 100%)`,
                position: 'relative',
                overflow: 'visible'
              }}>
                <div className="flag-emoji">{cuisine.flagEmoji}</div>
                <div className="category-content">
                  <h3 className="category-title">{cuisine.name}</h3>
                  <p className="category-description">{cuisine.description}</p>
                  <div className="category-stats">
                    <span>{cuisine.icon} 150+ recipes</span>
                    <span>⭐ 4.8/5</span>
                  </div>
                </div>
                
                {/* Hover Dishes Popup */}
                <div className="dishes-popup">
                  <div className="dishes-grid">
                    {cuisine.dishes.map((dish, dishIndex) => (
                      <div key={dishIndex} className="dish-preview">
                        <img src={dish.image} alt={dish.name} className="dish-image" />
                        <div className="dish-name">{dish.name}</div>
                      </div>
                    ))}
                  </div>
                </div>
            </div>
          ))}
        </div>
      </div>
      </section>

      {/* About Us Section */}
      <section id="about-us-section" className="about-us-section">
        <div className="about-us-content">
          <h2 className="section-title">About We Know</h2>
          <div className="about-us-grid">
            <div className="about-us-card">
              <div className="about-icon">🏢</div>
              <h3>Our Story</h3>
              <p>We Know was founded with a simple mission: to make cooking accessible to everyone. Our AI-powered platform helps you discover the perfect ingredients for any recipe, making your culinary journey effortless and enjoyable.</p>
            </div>
            
            <div className="about-us-card">
              <div className="about-icon">🎯</div>
              <h3>Our Mission</h3>
              <p>To revolutionize home cooking by providing intelligent ingredient recommendations, seamless delivery, and a community of food enthusiasts who share the joy of creating delicious meals.</p>
            </div>
            
            <div className="about-us-card">
              <div className="about-icon">🌟</div>
              <h3>Our Values</h3>
              <p>Quality, innovation, and customer satisfaction drive everything we do. We believe that great food starts with the right ingredients, and we're here to make that journey simple and delightful.</p>
            </div>
          </div>
          
          <div className="contact-social-section">
            <div className="contact-info">
              <h3>Get in Touch</h3>
              <div className="contact-details">
                <div className="contact-item">
                  <span className="contact-icon">📧</span>
                  <div>
                    <strong>Email:</strong>
                    <p>hello@weknow.com</p>
                  </div>
                </div>
                <div className="contact-item">
                  <span className="contact-icon">📞</span>
                  <div>
                    <strong>Phone:</strong>
                    <p>+1 (555) 123-4567</p>
                  </div>
                </div>
                <div className="contact-item">
                  <span className="contact-icon">📍</span>
                  <div>
                    <strong>Address:</strong>
                    <p>123 Food Street, Cuisine City, CC 12345</p>
                  </div>
                </div>
                <div className="contact-item">
                  <span className="contact-icon">🕒</span>
                  <div>
                    <strong>Hours:</strong>
                    <p>Mon-Fri: 9AM-6PM | Sat-Sun: 10AM-4PM</p>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="social-media">
              <h3>Follow Us</h3>
              <div className="social-links-grid">
                <a href="#" className="social-link-card">
                  <span className="social-icon">📘</span>
                  <span className="social-name">Facebook</span>
                  <span className="social-handle">@WeKnowFood</span>
                </a>
                <a href="#" className="social-link-card">
                  <span className="social-icon">📸</span>
                  <span className="social-name">Instagram</span>
                  <span className="social-handle">@WeKnowRecipes</span>
                </a>
                <a href="#" className="social-link-card">
                  <span className="social-icon">🐦</span>
                  <span className="social-name">Twitter</span>
                  <span className="social-handle">@WeKnowCooking</span>
                </a>
                <a href="#" className="social-link-card">
                  <span className="social-icon">💼</span>
                  <span className="social-name">LinkedIn</span>
                  <span className="social-handle">@WeKnowCompany</span>
                </a>
                <a href="#" className="social-link-card">
                  <span className="social-icon">📌</span>
                  <span className="social-name">Pinterest</span>
                  <span className="social-handle">@WeKnowInspiration</span>
                </a>
                <a href="#" className="social-link-card">
                  <span className="social-icon">📺</span>
                  <span className="social-name">YouTube</span>
                  <span className="social-handle">@WeKnowCooking</span>
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Comprehensive Footer - Swiggy Style */}
      <footer className="footer-section">
        <div className="footer-content">
          {/* App Download Section */}
          <div className="footer-app-download">
            <div className="download-text">
              <h3>For better experience, download the We Know app now</h3>
              <div className="download-buttons">
                <button className="download-btn android">
                  <span className="btn-icon">📱</span>
                  <div className="btn-text">
                    <span className="btn-title">Download Android App</span>
                    <span className="btn-subtitle">Get it on Google Play</span>
                  </div>
                </button>
                <button className="download-btn ios">
                  <span className="btn-icon">🍎</span>
                  <div className="btn-text">
                    <span className="btn-title">Download iOS App</span>
                    <span className="btn-subtitle">Download on App Store</span>
                  </div>
                </button>
              </div>
            </div>
          </div>

          {/* Main Footer Content */}
          <div className="footer-main">
            <div className="footer-column">
              <h4>Company</h4>
              <ul>
                <li><a href="#">About Us</a></li>
                <li><a href="#">We Know Corporate</a></li>
                <li><a href="#">Careers</a></li>
                <li><a href="#">Team</a></li>
                <li><a href="#">We Know One</a></li>
                <li><a href="#">We Know Instamart</a></li>
                <li><a href="#">We Know Dineout</a></li>
                <li><a href="#">We Know Genie</a></li>
                <li><a href="#">Minis</a></li>
                <li><a href="#">Pyng</a></li>
              </ul>
            </div>

            <div className="footer-column">
              <h4>Contact us</h4>
              <ul>
                <li><a href="#">Help & Support</a></li>
                <li><a href="#">Partner with us</a></li>
                <li><a href="#">Ride with us</a></li>
              </ul>
            </div>

            <div className="footer-column">
              <h4>Legal</h4>
              <ul>
                <li><a href="#">Terms & Conditions</a></li>
                <li><a href="#">Cookie Policy</a></li>
                <li><a href="#">Privacy Policy</a></li>
                <li><a href="#">Investor Relations</a></li>
              </ul>
            </div>

            <div className="footer-column">
              <h4>Life at We Know</h4>
              <ul>
                <li><a href="#">Explore with We Know</a></li>
                <li><a href="#">We Know News</a></li>
                <li><a href="#">Snackables</a></li>
              </ul>
            </div>

            <div className="footer-column">
              <h4>Available in:</h4>
              <ul className="cities-list">
                <li><a href="#">New York</a></li>
                <li><a href="#">Los Angeles</a></li>
                <li><a href="#">Chicago</a></li>
                <li><a href="#">Houston</a></li>
                <li><a href="#">Phoenix</a></li>
                <li><a href="#">Philadelphia</a></li>
              </ul>
              <p className="cities-count">679 cities</p>
            </div>

            <div className="footer-column">
              <h4>Social Links</h4>
              <ul className="social-links">
                <li><a href="#" className="social-link linkedin">LinkedIn</a></li>
                <li><a href="#" className="social-link instagram">Instagram</a></li>
                <li><a href="#" className="social-link facebook">Facebook</a></li>
                <li><a href="#" className="social-link pinterest">Pinterest</a></li>
              </ul>
            </div>
          </div>

          {/* Copyright Section */}
          <div className="footer-copyright">
            <p>© 2025 We Know Limited</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage; 