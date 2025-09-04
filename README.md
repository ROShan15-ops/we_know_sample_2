# We Know - Recipe Ingredient Generator

A full-stack web application that helps users input any dish name and receive a dynamically generated list of grocery ingredients using NLP and the Spoonacular API.

## 🌟 Features

- **Smart Dish Recognition**: Input any dish name and get ingredient lists
- **Dynamic Scaling**: Adjust ingredient quantities based on number of servings
- **NLP Processing**: Intelligent text cleaning and normalization
- **Responsive Design**: Works seamlessly on mobile and desktop
- **Copy/Download**: Easy sharing of grocery lists
- **Error Handling**: Graceful handling of API errors and missing recipes

## 🏗️ Project Structure

```
we-know/
├── backend/                 # Flask API server
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment variables template
├── frontend/               # React.js client
│   ├── public/             # Static assets
│   ├── src/                # React components
│   ├── package.json        # Node.js dependencies
│   └── README.md           # Frontend setup guide
└── README.md               # This file
```

## 🚀 Quick Start

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env and add your Spoonacular API key
   ```

5. Run the Flask server:
   ```bash
   python app.py
   ```

The backend will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

## 🔧 API Endpoints

### POST /ingredients
Fetches ingredient list for a given dish.

**Request Body:**
```json
{
  "dish_name": "Butter Chicken",
  "servings": 4
}
```

**Response:**
```json
{
  "success": true,
  "ingredients": [
    {
      "name": "chicken breast",
      "amount": 800,
      "unit": "g",
      "original_amount": 400,
      "original_unit": "g"
    }
  ],
  "recipe_info": {
    "title": "Butter Chicken",
    "original_servings": 2
  }
}
```

## 🛠️ Technologies Used

### Backend
- **Flask**: Python web framework
- **Spoonacular API**: Recipe and ingredient data
- **TextBlob**: NLP text processing
- **python-dotenv**: Environment variable management
- **flask-cors**: Cross-origin resource sharing

### Frontend
- **React.js**: Frontend framework
- **Axios**: HTTP client for API calls
- **CSS3**: Styling (with responsive design)
- **React Hooks**: State management

## 🔑 Environment Variables

Create a `.env` file in the backend directory:

```env
SPOONACULAR_API_KEY=your_api_key_here
FLASK_ENV=development
```

Get your Spoonacular API key from: https://spoonacular.com/food-api

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📱 Features

- **Dish Input**: Type any dish name
- **Serving Adjustment**: Scale ingredients from 1-10 servings
- **Ingredient List**: Detailed quantities and units
- **Copy to Clipboard**: One-click copying of grocery list
- **Download**: Export as text file
- **Loading States**: Visual feedback during API calls
- **Error Handling**: User-friendly error messages
- **Responsive Design**: Mobile-first approach

## 🚀 Deployment

### Backend (Render/Railway)
1. Push code to GitHub
2. Connect repository to Render/Railway
3. Set environment variables
4. Deploy

### Frontend (Vercel/Netlify)
1. Push code to GitHub
2. Connect repository to Vercel/Netlify
3. Set build command: `npm run build`
4. Deploy

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [Spoonacular API](https://spoonacular.com/food-api) for recipe data
- [TextBlob](https://textblob.readthedocs.io/) for NLP processing 