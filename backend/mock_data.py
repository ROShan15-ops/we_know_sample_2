# Mock shop inventory data
MOCK_SHOPS = {
    "Fresh Mart": {
        "location": {"lat": 37.7749, "lng": -122.4194},  # San Francisco
        "inventory": [
            "chicken", "rice", "onion", "tomato", "garlic", "ginger", "turmeric", 
            "cumin", "coriander", "cardamom", "cinnamon", "cloves", "bay leaves",
            "mint", "cilantro", "lemon", "yogurt", "ghee", "oil", "salt", "pepper",
            "flour", "yeast", "sugar", "milk", "butter", "cheese", "eggs", "bread",
            "pasta", "olive oil", "basil", "oregano", "parmesan", "mozzarella",
            "beef", "pork", "lamb", "fish", "shrimp", "vegetables", "fruits",
            "heavy cream", "whipping cream", "chocolate", "dark chocolate", "vanilla extract",
            "vanilla", "cocoa powder", "baking soda", "baking powder", "vanilla bean"
        ]
    },
    "Super Foods": {
        "location": {"lat": 37.7849, "lng": -122.4094},
        "inventory": [
            "chicken", "rice", "onion", "tomato", "garlic", "ginger", "turmeric",
            "cumin", "coriander", "cardamom", "cinnamon", "cloves", "bay leaves",
            "mint", "cilantro", "lemon", "yogurt", "ghee", "oil", "salt", "pepper",
            "flour", "yeast", "sugar", "milk", "butter", "cheese", "eggs", "bread",
            "pasta", "olive oil", "basil", "oregano", "parmesan", "mozzarella",
            "beef", "pork", "lamb", "fish", "shrimp", "vegetables", "fruits",
            "saffron", "rose water", "cashews", "almonds", "raisins",
            "heavy cream", "whipping cream", "chocolate", "dark chocolate", "vanilla extract",
            "vanilla", "cocoa powder", "baking soda", "baking powder", "vanilla bean"
        ]
    },
    "Local Grocery": {
        "location": {"lat": 37.7649, "lng": -122.4294},
        "inventory": [
            "chicken", "rice", "onion", "tomato", "garlic", "ginger", "turmeric",
            "cumin", "coriander", "cardamom", "cinnamon", "cloves", "bay leaves",
            "mint", "cilantro", "lemon", "yogurt", "ghee", "oil", "salt", "pepper",
            "flour", "yeast", "sugar", "milk", "butter", "cheese", "eggs", "bread",
            "pasta", "olive oil", "basil", "oregano", "parmesan", "mozzarella"
        ]
    },
    "Asian Market": {
        "location": {"lat": 37.7949, "lng": -122.3994},
        "inventory": [
            "chicken", "rice", "onion", "tomato", "garlic", "ginger", "turmeric",
            "cumin", "coriander", "cardamom", "cinnamon", "cloves", "bay leaves",
            "mint", "cilantro", "lemon", "yogurt", "ghee", "oil", "salt", "pepper",
            "saffron", "rose water", "cashews", "almonds", "raisins", "basmati rice",
            "jasmine rice", "curry leaves", "tamarind", "coconut milk", "fish sauce",
            "soy sauce", "sesame oil", "mirin", "sake", "miso", "nori", "wasabi"
        ]
    },
    "Organic Corner": {
        "location": {"lat": 37.7549, "lng": -122.4394},
        "inventory": [
            "chicken", "rice", "onion", "tomato", "garlic", "ginger", "turmeric",
            "cumin", "coriander", "cardamom", "cinnamon", "cloves", "bay leaves",
            "mint", "cilantro", "lemon", "yogurt", "ghee", "oil", "salt", "pepper",
            "flour", "yeast", "sugar", "milk", "butter", "cheese", "eggs", "bread",
            "pasta", "olive oil", "basil", "oregano", "parmesan", "mozzarella",
            "organic vegetables", "organic fruits", "quinoa", "chia seeds", "flax seeds"
        ]
    }
}

# Mock delivery agents
DELIVERY_AGENTS = [
    {"id": "agent_001", "name": "Agent A", "status": "available", "current_location": {"lat": 37.7749, "lng": -122.4194}},
    {"id": "agent_002", "name": "Agent B", "status": "available", "current_location": {"lat": 37.7849, "lng": -122.4094}},
    {"id": "agent_003", "name": "Agent C", "status": "available", "current_location": {"lat": 37.7649, "lng": -122.4294}},
    {"id": "agent_004", "name": "Agent D", "status": "available", "current_location": {"lat": 37.7949, "lng": -122.3994}},
    {"id": "agent_005", "name": "Agent E", "status": "available", "current_location": {"lat": 37.7549, "lng": -122.4394}}
]

# Predefined recipes with unique ingredients for different pizza varieties
PIZZA_RECIPES = {
    'margherita': {
        'id': 658615,
        'title': 'Margherita Pizza',
        'ingredients': [
            {'ingredient': 'pizza dough', 'quantity': 1, 'unit': 'piece'},
            {'ingredient': 'fresh mozzarella', 'quantity': 200, 'unit': 'grams'},
            {'ingredient': 'tomato sauce', 'quantity': 150, 'unit': 'ml'},
            {'ingredient': 'fresh basil leaves', 'quantity': 20, 'unit': 'grams'},
            {'ingredient': 'extra virgin olive oil', 'quantity': 30, 'unit': 'ml'},
            {'ingredient': 'salt', 'quantity': 5, 'unit': 'grams'},
            {'ingredient': 'black pepper', 'quantity': 3, 'unit': 'grams'}
        ]
    },
    'pepperoni': {
        'id': 716300,
        'title': 'Pepperoni Pizza',
        'ingredients': [
            {'ingredient': 'pizza dough', 'quantity': 1, 'unit': 'piece'},
            {'ingredient': 'pepperoni slices', 'quantity': 150, 'unit': 'grams'},
            {'ingredient': 'mozzarella cheese', 'quantity': 200, 'unit': 'grams'},
            {'ingredient': 'tomato sauce', 'quantity': 200, 'unit': 'ml'},
            {'ingredient': 'parmesan cheese', 'quantity': 50, 'unit': 'grams'},
            {'ingredient': 'oregano', 'quantity': 5, 'unit': 'grams'},
            {'ingredient': 'garlic powder', 'quantity': 3, 'unit': 'grams'},
            {'ingredient': 'red pepper flakes', 'quantity': 2, 'unit': 'grams'}
        ]
    }
    # Add more pizza varieties as needed
} 