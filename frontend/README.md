# We Know - Frontend

React.js frontend for the We Know recipe ingredient generator application.

## Features

- 🍽️ **Smart Dish Input**: Type any dish name and get ingredient lists
- 📊 **Dynamic Scaling**: Adjust quantities based on number of servings (1-10)
- 📱 **Responsive Design**: Works perfectly on mobile and desktop
- 📋 **Copy to Clipboard**: One-click copying of grocery lists
- 💾 **Download**: Export grocery lists as text files
- 🔄 **Recent Searches**: Quick access to previously searched dishes
- ⚡ **Real-time Feedback**: Loading states and error handling

## Quick Start

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm start
   ```

3. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm test` - Launches the test runner
- `npm run build` - Builds the app for production
- `npm run eject` - Ejects from Create React App (one-way operation)

## Dependencies

- **React 18** - Frontend framework
- **Axios** - HTTP client for API calls
- **react-copy-to-clipboard** - Copy functionality
- **CSS3** - Modern styling with responsive design

## Project Structure

```
src/
├── App.js          # Main application component
├── App.css         # Application styles
├── index.js        # React entry point
└── index.css       # Base styles
```

## API Integration

The frontend communicates with the Flask backend at `http://localhost:5000`:

- **POST /ingredients** - Fetch ingredients for a dish
- **GET /health** - Health check endpoint

## Features in Detail

### Dish Input
- Text input field for dish names
- Supports any cuisine or dish type
- Real-time validation

### Serving Adjustment
- Dropdown selection (1-10 servings)
- Dynamic ingredient scaling
- Clear display of original vs. scaled quantities

### Recent Searches
- Automatically saves recent searches
- Click to quickly re-search
- Stored in localStorage

### Copy & Download
- Copy entire grocery list to clipboard
- Download as formatted text file
- Includes recipe info and serving details

### Error Handling
- User-friendly error messages
- Network error handling
- Recipe not found scenarios

### Responsive Design
- Mobile-first approach
- Tablet and desktop optimized
- Touch-friendly interface

## Development

### Environment Variables
The app uses a proxy configuration in `package.json` to forward API calls to the backend during development.

### Styling
- Custom CSS with modern design
- Gradient backgrounds and glassmorphism effects
- Smooth animations and transitions
- Mobile-responsive breakpoints

## Deployment

### Build for Production
```bash
npm run build
```

### Deploy to Vercel/Netlify
1. Push code to GitHub
2. Connect repository to deployment platform
3. Set build command: `npm run build`
4. Deploy

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request 