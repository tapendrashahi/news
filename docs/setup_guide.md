# Developer Setup Guide

## Prerequisites

### Required Software
- **Python**: 3.10 or higher
- **Node.js**: 18.x or higher
- **npm**: 9.x or higher
- **Git**: Latest version
- **Code Editor**: VS Code (recommended)

### Recommended Tools
- **Postman**: API testing
- **Chrome DevTools**: Frontend debugging
- **React DevTools**: React debugging

---

## Backend Setup (Django)

### 1. Clone the Repository
```bash
cd /home/tapendra/Downloads/projects/news
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### 3. Install Backend Dependencies
```bash
pip install -r requirements.txt

# Install additional packages for React integration
pip install djangorestframework
pip install django-cors-headers
pip install markdown
pip install django-filter
```

### 4. Update requirements.txt
```bash
pip freeze > requirements.txt
```

### 5. Configure Environment Variables
Create a `.env` file in the project root:
```bash
touch .env
```

Add the following to `.env`:
```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (using SQLite for development)
DATABASE_URL=sqlite:///db.sqlite3

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Media Files
MEDIA_URL=/media/
MEDIA_ROOT=media/

# Static Files
STATIC_URL=/static/
STATIC_ROOT=staticfiles/
```

### 6. Run Migrations
```bash
python manage.py migrate
```

### 7. Create Superuser
```bash
python manage.py createsuperuser
```

### 8. Load Sample Data (Optional)
```bash
# If you have fixtures
python manage.py loaddata sample_data.json
```

### 9. Run Development Server
```bash
python manage.py runserver
```

Backend should be running at: `http://localhost:8000`

---

## Frontend Setup (React)

### 1. Create Frontend Directory
```bash
mkdir frontend
cd frontend
```

### 2. Initialize npm Project
```bash
npm init -y
```

### 3. Install React Dependencies
```bash
# Core dependencies
npm install react react-dom react-router-dom

# API and state management
npm install axios @tanstack/react-query

# Utilities
npm install prop-types
```

### 4. Install Development Dependencies
```bash
# Webpack and loaders
npm install --save-dev webpack webpack-cli webpack-dev-server
npm install --save-dev html-webpack-plugin
npm install --save-dev style-loader css-loader
npm install --save-dev file-loader url-loader

# Babel
npm install --save-dev @babel/core @babel/preset-env @babel/preset-react
npm install --save-dev babel-loader

# Code quality
npm install --save-dev eslint eslint-plugin-react
npm install --save-dev prettier

# Testing (optional for now)
npm install --save-dev jest @testing-library/react @testing-library/jest-dom
```

### 5. Create Frontend Structure
```bash
# Create directories
mkdir -p public src/components src/pages src/services src/hooks src/utils src/styles

# Create entry files
touch public/index.html
touch src/index.jsx
touch src/App.jsx
```

### 6. Create Configuration Files

#### `frontend/.env`
```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_MEDIA_URL=http://localhost:8000/media
```

#### `frontend/.babelrc`
```json
{
  "presets": [
    "@babel/preset-env",
    "@babel/preset-react"
  ]
}
```

#### `frontend/.eslintrc.js`
```javascript
module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
  ],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true,
    },
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
  rules: {
    'react/prop-types': 'warn',
    'no-unused-vars': 'warn',
  },
};
```

#### `frontend/.prettierrc`
```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5"
}
```

#### `frontend/webpack.config.js`
```javascript
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: './src/index.jsx',
  output: {
    path: path.resolve(__dirname, 'build'),
    filename: 'bundle.[contenthash].js',
    publicPath: '/',
    clean: true,
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
        },
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
      {
        test: /\.(png|svg|jpg|jpeg|gif)$/i,
        type: 'asset/resource',
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './public/index.html',
    }),
  ],
  devServer: {
    historyApiFallback: true,
    port: 3000,
    hot: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/media': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
};
```

### 7. Update package.json Scripts
Edit `frontend/package.json`:
```json
{
  "scripts": {
    "start": "webpack serve --mode development",
    "build": "webpack --mode production",
    "test": "jest",
    "lint": "eslint src/",
    "format": "prettier --write \"src/**/*.{js,jsx,css}\""
  }
}
```

### 8. Create Basic Files

#### `frontend/public/index.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>News Portal</title>
</head>
<body>
    <div id="root"></div>
</body>
</html>
```

#### `frontend/src/index.jsx`
```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/index.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

#### `frontend/src/App.jsx`
```javascript
import React from 'react';

function App() {
  return (
    <div className="app">
      <h1>News Portal - React Frontend</h1>
      <p>Welcome to the news portal!</p>
    </div>
  );
}

export default App;
```

#### `frontend/src/styles/index.css`
```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.app {
  padding: 20px;
}
```

### 9. Run Frontend Development Server
```bash
cd frontend
npm start
```

Frontend should be running at: `http://localhost:3000`

---

## Django Configuration for React

### 1. Update Django Settings

Edit `gis/settings.py`:

```python
# Add REST Framework and CORS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Add this
    'corsheaders',     # Add this
    'news',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Add this (near top)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS Settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True

# REST Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# React Frontend
REACT_APP_DIR = BASE_DIR / 'frontend'

STATICFILES_DIRS = [
    BASE_DIR / 'news' / 'static',
]

# For production build
# STATICFILES_DIRS = [
#     BASE_DIR / 'news' / 'static',
#     REACT_APP_DIR / 'build' / 'static',
# ]
```

### 2. Create API App Structure

Create `news/api.py`:
```bash
touch news/api.py
touch news/serializers.py
```

### 3. Update URLs

Edit `gis/urls.py`:
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('news.api_urls')),  # API endpoints
    path('', include('news.urls')),          # Frontend routes
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## Development Workflow

### Running Both Servers

**Terminal 1 - Backend:**
```bash
cd /home/tapendra/Downloads/projects/news
source venv/bin/activate
python manage.py runserver
```

**Terminal 2 - Frontend:**
```bash
cd /home/tapendra/Downloads/projects/news/frontend
npm start
```

### Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api
- **Django Admin**: http://localhost:8000/admin

---

## Git Configuration

### Create .gitignore
```bash
# Python
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.sqlite3
*.db

# Django
*.log
local_settings.py
db.sqlite3
media/
staticfiles/

# Environment
.env
.env.local

# Node
frontend/node_modules/
frontend/build/
frontend/dist/
npm-debug.log*

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
```

### Initialize Git (if not already done)
```bash
git init
git add .
git commit -m "Initial commit with React integration setup"
```

---

## Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

#### CORS Errors
- Check `CORS_ALLOWED_ORIGINS` in Django settings
- Ensure `corsheaders` middleware is added
- Clear browser cache

#### Module Not Found
```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend && npm install
```

#### Database Issues
```bash
# Reset database
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## Next Steps

1. ✅ Complete this setup guide
2. 📝 Create API serializers and views
3. 🎨 Build React components
4. 🔌 Connect frontend to backend API
5. 🎨 Add styling
6. 🧪 Write tests
7. 🚀 Deploy to production

---

## Useful Commands

### Django
```bash
# Create migrations
python manage.py makemigrations

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run shell
python manage.py shell
```

### React
```bash
# Install package
npm install package-name

# Remove package
npm uninstall package-name

# Update packages
npm update

# Audit packages
npm audit
```

---

**Last Updated**: December 4, 2025  
**Version**: 1.0
