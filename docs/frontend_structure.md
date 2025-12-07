# Frontend Directory Structure

## Overview
This document details the complete directory structure for the React frontend application.

## Complete Directory Tree

```
frontend/
├── public/
│   ├── index.html              # HTML template
│   ├── favicon.ico             # Site favicon
│   ├── manifest.json           # PWA manifest
│   ├── robots.txt              # SEO robots file
│   └── assets/
│       ├── images/             # Static images
│       └── fonts/              # Custom fonts
│
├── src/
│   ├── index.jsx               # Application entry point
│   ├── App.jsx                 # Root component
│   ├── routes.jsx              # Route definitions
│   │
│   ├── components/             # Reusable components
│   │   ├── common/            # Generic reusable components
│   │   │   ├── Button/
│   │   │   │   ├── Button.jsx
│   │   │   │   ├── Button.module.css
│   │   │   │   └── index.js
│   │   │   ├── Card/
│   │   │   │   ├── Card.jsx
│   │   │   │   └── index.js
│   │   │   ├── Input/
│   │   │   ├── Modal/
│   │   │   ├── Loader/
│   │   │   ├── ErrorBoundary/
│   │   │   ├── Pagination/
│   │   │   └── SearchBar/
│   │   │
│   │   ├── layout/            # Layout components
│   │   │   ├── Header/
│   │   │   │   ├── Header.jsx
│   │   │   │   ├── Header.module.css
│   │   │   │   └── index.js
│   │   │   ├── Footer/
│   │   │   │   ├── Footer.jsx
│   │   │   │   └── index.js
│   │   │   ├── Navbar/
│   │   │   ├── Sidebar/
│   │   │   ├── Container/
│   │   │   └── Layout.jsx     # Main layout wrapper
│   │   │
│   │   └── news/              # News-specific components
│   │       ├── NewsCard/
│   │       │   ├── NewsCard.jsx
│   │       │   ├── NewsCard.module.css
│   │       │   └── index.js
│   │       ├── NewsList/
│   │       ├── NewsGrid/
│   │       ├── FeaturedNews/
│   │       ├── CategoryBadge/
│   │       ├── ShareButtons/
│   │       ├── CommentForm/
│   │       ├── CommentList/
│   │       ├── NewsletterForm/
│   │       ├── TeamMemberCard/
│   │       └── RelatedNews/
│   │
│   ├── pages/                  # Page components
│   │   ├── Home/
│   │   │   ├── Home.jsx
│   │   │   ├── Home.module.css
│   │   │   └── index.js
│   │   ├── NewsDetail/
│   │   │   ├── NewsDetail.jsx
│   │   │   └── index.js
│   │   ├── Category/
│   │   │   ├── Category.jsx
│   │   │   └── index.js
│   │   ├── Search/
│   │   ├── About/
│   │   ├── Team/
│   │   ├── PrivacyPolicy/
│   │   ├── TermsOfService/
│   │   ├── EthicsPolicy/
│   │   ├── EditorialGuidelines/
│   │   ├── CookiePolicy/
│   │   └── NotFound/          # 404 page
│   │
│   ├── services/               # API service layer
│   │   ├── api.js             # Axios instance configuration
│   │   ├── newsService.js     # News API calls
│   │   ├── teamService.js     # Team API calls
│   │   ├── commentService.js  # Comment API calls
│   │   ├── subscriberService.js
│   │   └── searchService.js
│   │
│   ├── hooks/                  # Custom React hooks
│   │   ├── useNews.js         # Fetch news data
│   │   ├── useNewsDetail.js   # Fetch single news
│   │   ├── useCategories.js   # Fetch categories
│   │   ├── useTeam.js         # Fetch team members
│   │   ├── useSearch.js       # Search functionality
│   │   ├── usePagination.js   # Pagination logic
│   │   ├── useDebounce.js     # Debounce hook
│   │   └── useMediaQuery.js   # Responsive design hook
│   │
│   ├── context/                # React Context
│   │   ├── NewsContext.jsx    # News state management
│   │   ├── ThemeContext.jsx   # Theme (light/dark mode)
│   │   └── AuthContext.jsx    # Authentication (future)
│   │
│   ├── utils/                  # Utility functions
│   │   ├── dateFormatter.js   # Date formatting
│   │   ├── textTruncate.js    # Text manipulation
│   │   ├── urlHelpers.js      # URL generation
│   │   ├── validation.js      # Form validation
│   │   └── constants.js       # App constants
│   │
│   ├── styles/                 # Global styles
│   │   ├── index.css          # Global CSS
│   │   ├── variables.css      # CSS variables
│   │   ├── reset.css          # CSS reset
│   │   └── tailwind.css       # Tailwind imports (if using)
│   │
│   └── assets/                 # Asset files
│       ├── images/            # Images used in components
│       ├── icons/             # SVG icons
│       └── logo/              # Logo files
│
├── tests/                      # Test files
│   ├── unit/                  # Unit tests
│   │   ├── components/
│   │   └── utils/
│   ├── integration/           # Integration tests
│   └── e2e/                   # End-to-end tests
│
├── config/                     # Configuration files
│   ├── webpack.config.js      # Webpack configuration
│   ├── webpack.dev.js         # Development config
│   └── webpack.prod.js        # Production config
│
├── .babelrc                    # Babel configuration
├── .eslintrc.js               # ESLint configuration
├── .prettierrc                # Prettier configuration
├── .gitignore                 # Git ignore rules
├── package.json               # Dependencies and scripts
├── package-lock.json          # Lock file
├── .env.example               # Environment variables example
├── .env                       # Environment variables (not in git)
└── README.md                  # Frontend documentation
```

## File Descriptions

### Root Files

#### `src/index.jsx`
Entry point of the React application. Renders the App component.

#### `src/App.jsx`
Root component that sets up routing, context providers, and global layout.

#### `src/routes.jsx`
Centralized route definitions for the application.

### Components Structure

#### Common Components (`src/components/common/`)
Reusable UI components used throughout the application:
- **Button**: Customizable button component
- **Card**: Content card wrapper
- **Input**: Form input fields
- **Modal**: Modal dialog component
- **Loader**: Loading spinner/skeleton
- **ErrorBoundary**: Error handling wrapper
- **Pagination**: Page navigation component
- **SearchBar**: Search input component

#### Layout Components (`src/components/layout/`)
Structural components:
- **Header**: Site header with logo and navigation
- **Footer**: Site footer with links
- **Navbar**: Main navigation bar
- **Sidebar**: Side navigation (if needed)
- **Container**: Content wrapper with max-width
- **Layout**: Main layout wrapper component

#### News Components (`src/components/news/`)
News-specific components:
- **NewsCard**: Individual news item card
- **NewsList**: List view of news items
- **NewsGrid**: Grid view of news items
- **FeaturedNews**: Featured news section
- **CategoryBadge**: Category label/badge
- **ShareButtons**: Social media share buttons
- **CommentForm**: Comment submission form
- **CommentList**: List of comments
- **NewsletterForm**: Newsletter subscription form
- **TeamMemberCard**: Team member profile card
- **RelatedNews**: Related news suggestions

### Pages (`src/pages/`)

Each page is a route-level component:
- **Home**: Landing page with latest news
- **NewsDetail**: Individual news article page
- **Category**: Category-filtered news list
- **Search**: Search results page
- **About**: About us page
- **Team**: Team members page
- **PrivacyPolicy**: Privacy policy page
- **TermsOfService**: Terms of service page
- **EthicsPolicy**: Ethics policy page
- **EditorialGuidelines**: Editorial guidelines page
- **CookiePolicy**: Cookie policy page
- **NotFound**: 404 error page

### Services (`src/services/`)

API service layer for backend communication:

#### `api.js`
```javascript
// Axios instance with base configuration
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
// Response interceptor
export default api;
```

#### `newsService.js`
- `getNews()` - Fetch news list
- `getNewsDetail(slug)` - Fetch single news
- `getNewsByCategory(category)` - Filter by category
- `searchNews(query)` - Search news

#### `commentService.js`
- `getComments(newsId)` - Fetch comments
- `addComment(newsId, data)` - Add comment

#### `subscriberService.js`
- `subscribe(email)` - Newsletter subscription

### Hooks (`src/hooks/`)

Custom React hooks for reusable logic:
- **useNews**: Fetch and manage news data
- **useNewsDetail**: Fetch single news article
- **useCategories**: Fetch category data
- **useTeam**: Fetch team members
- **useSearch**: Search functionality
- **usePagination**: Pagination state management
- **useDebounce**: Debounce user input
- **useMediaQuery**: Responsive breakpoints

### Context (`src/context/`)

React Context for global state:
- **NewsContext**: News-related state
- **ThemeContext**: Theme preferences
- **AuthContext**: Authentication state (future)

### Utils (`src/utils/`)

Utility functions:
- **dateFormatter**: Format dates (e.g., "2 days ago")
- **textTruncate**: Truncate long text
- **urlHelpers**: Generate URLs
- **validation**: Form validation rules
- **constants**: App-wide constants

### Styles (`src/styles/`)

Global styling:
- **index.css**: Global styles
- **variables.css**: CSS custom properties
- **reset.css**: CSS normalization
- **tailwind.css**: Tailwind CSS imports

## Configuration Files

### `package.json`
```json
{
  "name": "news-frontend",
  "version": "1.0.0",
  "description": "React frontend for Django news application",
  "scripts": {
    "start": "webpack serve --config config/webpack.dev.js",
    "build": "webpack --config config/webpack.prod.js",
    "test": "jest",
    "lint": "eslint src/",
    "format": "prettier --write \"src/**/*.{js,jsx}\""
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.0",
    "@tanstack/react-query": "^5.12.0"
  },
  "devDependencies": {
    "@babel/core": "^7.23.0",
    "@babel/preset-env": "^7.23.0",
    "@babel/preset-react": "^7.23.0",
    "babel-loader": "^9.1.3",
    "webpack": "^5.89.0",
    "webpack-cli": "^5.1.4",
    "webpack-dev-server": "^4.15.0",
    "css-loader": "^6.8.1",
    "style-loader": "^3.3.3",
    "html-webpack-plugin": "^5.5.4",
    "eslint": "^8.54.0",
    "prettier": "^3.1.0"
  }
}
```

### `.babelrc`
```json
{
  "presets": [
    "@babel/preset-env",
    "@babel/preset-react"
  ]
}
```

### `.eslintrc.js`
```javascript
module.exports = {
  env: {
    browser: true,
    es2021: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
  ],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
  },
  rules: {
    'react/prop-types': 'warn',
  },
};
```

## Naming Conventions

### Files
- **Components**: PascalCase (e.g., `NewsCard.jsx`)
- **Utilities**: camelCase (e.g., `dateFormatter.js`)
- **Styles**: Match component name (e.g., `NewsCard.module.css`)

### Components
- **Components**: PascalCase (e.g., `NewsCard`)
- **Props**: camelCase (e.g., `newsData`)
- **Functions**: camelCase (e.g., `handleClick`)

### CSS
- **Classes**: kebab-case or BEM methodology
- **CSS Modules**: camelCase in JS, kebab-case in CSS

## Best Practices

1. **Component Organization**: One component per file
2. **Index Files**: Export components from index.js
3. **Prop Types**: Define prop types for all components
4. **CSS Modules**: Use CSS modules for component styles
5. **Code Splitting**: Lazy load routes and heavy components
6. **Error Handling**: Use ErrorBoundary components
7. **Testing**: Test files adjacent to components
8. **Documentation**: Add JSDoc comments for complex functions

## Next Steps

1. Create the frontend directory structure
2. Initialize npm project
3. Install dependencies
4. Set up Webpack configuration
5. Create base components
6. Implement routing
7. Connect to Django API

---

**Last Updated**: December 4, 2025  
**Version**: 1.0
