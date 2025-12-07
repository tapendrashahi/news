# News Portal - React Frontend

## Overview
This is the React frontend for the Django News Portal application. It provides a modern, responsive user interface for browsing news articles.

## Tech Stack
- **React 18** - UI framework
- **React Router v6** - Client-side routing
- **Axios** - HTTP client
- **React Query** - Server state management
- **Webpack 5** - Module bundler
- **Babel** - JavaScript transpiler

## Prerequisites
- Node.js 18.x or higher
- npm 9.x or higher
- Backend Django server running on `http://localhost:8000`

## Installation

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure Environment
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_MEDIA_URL=http://localhost:8000/media
```

### 3. Run Development Server
```bash
npm start
```

The app will open at `http://localhost:3000`

## Available Scripts

### Development
```bash
npm start       # Start development server
npm run watch   # Watch mode for file changes
```

### Production
```bash
npm run build   # Build for production
```

### Code Quality
```bash
npm run lint       # Run ESLint
npm run lint:fix   # Fix ESLint errors
npm run format     # Format code with Prettier
```

### Testing
```bash
npm test        # Run tests
```

## Project Structure

```
frontend/
├── public/              # Static files
├── src/
│   ├── components/     # Reusable components
│   │   ├── common/    # Generic components
│   │   ├── layout/    # Layout components
│   │   └── news/      # News-specific components
│   ├── pages/         # Page components
│   ├── services/      # API services
│   ├── hooks/         # Custom hooks
│   ├── utils/         # Utility functions
│   ├── styles/        # Global styles
│   ├── App.jsx        # Root component
│   ├── routes.jsx     # Route definitions
│   └── index.jsx      # Entry point
├── config/            # Webpack configs
└── package.json       # Dependencies
```

## Features

### Current Features
- ✅ Home page with latest news
- ✅ Responsive layout with header and footer
- ✅ React Router navigation
- ✅ API integration ready
- ✅ Loading states
- ✅ Error handling

### Upcoming Features
- 📝 News detail page
- 📝 Category filtering
- 📝 Search functionality
- 📝 Comments system
- 📝 Share buttons
- 📝 Newsletter subscription
- 📝 Team member profiles

## API Integration

The app connects to the Django backend API:

### Base URL
```javascript
const API_URL = process.env.REACT_APP_API_URL;
```

### Example API Calls
```javascript
import { newsService } from './services/newsService';

// Get all news
const news = await newsService.getNews();

// Get news by category
const techNews = await newsService.getNewsByCategory('tech');

// Search news
const results = await newsService.searchNews('technology');
```

## Development

### Adding a New Page
1. Create component in `src/pages/`
2. Add route in `src/routes.jsx`
3. Add navigation link in Header component

### Adding a New Component
1. Create folder in appropriate location
2. Create component file (e.g., `Button.jsx`)
3. Create styles (optional)
4. Export from index.js

### API Service Pattern
```javascript
// src/services/myService.js
import api from './api';

export const myService = {
  getData: async () => {
    const response = await api.get('/endpoint/');
    return response.data;
  },
};
```

## Styling

### CSS Variables
Global CSS variables are defined in `src/styles/index.css`:
```css
:root {
  --primary-color: #1a73e8;
  --text-color: #202124;
  /* ... */
}
```

### Inline Styles vs CSS
- Use inline styles for simple, component-specific styles
- Use CSS files for complex or shared styles
- Consider CSS Modules for component-scoped styles

## Build Configuration

### Development Build
- Source maps enabled
- Hot module replacement
- Proxy to Django backend

### Production Build
- Minified and optimized
- Code splitting
- Hashed filenames for caching

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

### CORS Errors
Ensure Django backend has CORS configured:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
```

### Module Not Found
```bash
npm install
```

## Deployment

### Build for Production
```bash
npm run build
```

This creates a `build/` directory with optimized files.

### Django Integration
The build files should be copied to Django's static directory:
```bash
cp -r build/* ../static/react/
```

## Contributing

1. Follow the existing code structure
2. Use ESLint and Prettier
3. Write meaningful commit messages
4. Test before committing

## License
MIT

## Support
For issues or questions, please contact the development team.
