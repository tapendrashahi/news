# Django News Portal with React Frontend

## Overview
A modern news portal application built with Django backend and React frontend. Features include news articles, categories, comments, team member profiles, and newsletter subscription.

## Architecture
- **Backend**: Django 5.2 + Django REST Framework
- **Frontend**: React 18 + React Router + React Query
- **Database**: SQLite (development) / PostgreSQL (production)
- **API**: RESTful API with JSON responses

## Project Structure

```
news/
├── backend/                    # Django project
│   ├── gis/                   # Main Django app
│   ├── news/                  # News application
│   │   ├── models.py         # Data models
│   │   ├── views.py          # View functions
│   │   ├── admin.py          # Admin configuration
│   │   ├── serializers.py    # API serializers
│   │   └── api.py            # API endpoints
│   └── manage.py
│
├── frontend/                   # React application
│   ├── src/
│   │   ├── components/       # Reusable components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API services
│   │   └── hooks/           # Custom hooks
│   ├── public/              # Static files
│   └── package.json
│
├── docs/                       # Documentation
│   ├── react_integration_plan.md
│   ├── frontend_structure.md
│   ├── api_documentation.md
│   └── setup_guide.md
│
├── media/                      # User uploads
├── static/                     # Static files
└── requirements.txt            # Python dependencies
```

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm 9+

### Automated Setup
```bash
# Make setup script executable (if not already)
chmod +x setup.sh

# Run setup script
./setup.sh
```

This will:
1. Create Python virtual environment
2. Install Python dependencies
3. Install Node.js dependencies
4. Run database migrations
5. Create superuser (optional)

### Manual Setup

#### Backend
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Additional packages for React integration
pip install djangorestframework django-cors-headers

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

#### Frontend
```bash
cd frontend
npm install
cp .env.example .env
```

## Running the Application

### Development Mode

#### Option 1: Run Both Servers (Automated)
```bash
./dev_server.sh
```

#### Option 2: Run Servers Separately

**Terminal 1 - Django Backend:**
```bash
source venv/bin/activate
python manage.py runserver
```

**Terminal 2 - React Frontend:**
```bash
cd frontend
npm start
```

### Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api
- **Django Admin**: http://localhost:8000/admin

## Production Build

### Build Frontend
```bash
./build_frontend.sh
```
Or manually:
```bash
cd frontend
npm run build
```

### Deploy
1. Build React frontend
2. Copy build files to Django static directory
3. Collect static files: `python manage.py collectstatic`
4. Configure production settings
5. Deploy to server

## Features

### Current Features
✅ News article management  
✅ Category filtering  
✅ Team member profiles  
✅ Comment system  
✅ Share counters  
✅ Newsletter subscription  
✅ Django admin panel  
✅ RESTful API  
✅ React frontend (basic)  

### In Development
🔨 Full React UI implementation  
🔨 Advanced search functionality  
🔨 User authentication  
🔨 Rich text editor  
🔨 Image optimization  

## API Documentation

Full API documentation is available in `docs/api_documentation.md`

### Key Endpoints

```
GET    /api/news/                    # List all news
GET    /api/news/{slug}/             # Get news detail
GET    /api/news/category/{cat}/    # Filter by category
GET    /api/news/search/?q=query    # Search news
POST   /api/news/{id}/comment/      # Add comment
POST   /api/subscribe/               # Subscribe to newsletter
GET    /api/team/                    # List team members
GET    /api/categories/              # Get categories
```

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[React Integration Plan](docs/react_integration_plan.md)** - Architecture and implementation plan
- **[Frontend Structure](docs/frontend_structure.md)** - React app structure
- **[API Documentation](docs/api_documentation.md)** - REST API endpoints
- **[Setup Guide](docs/setup_guide.md)** - Detailed setup instructions

## Development Workflow

### Adding New Features

1. **Backend (Django)**
   - Add/update models in `news/models.py`
   - Create serializers in `news/serializers.py`
   - Add API views in `news/api.py`
   - Update URLs in `news/api_urls.py`

2. **Frontend (React)**
   - Create components in `frontend/src/components/`
   - Add pages in `frontend/src/pages/`
   - Create API services in `frontend/src/services/`
   - Update routes in `frontend/src/routes.jsx`

### Code Quality

```bash
# Backend
python manage.py test           # Run tests
black .                         # Format code
pylint news/                    # Lint code

# Frontend
cd frontend
npm test                        # Run tests
npm run lint                    # Lint code
npm run format                  # Format code
```

## Environment Variables

### Backend (.env)
```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_MEDIA_URL=http://localhost:8000/media
```

## Database Models

- **News**: Article content, metadata, and relationships
- **TeamMember**: Staff profiles and information
- **Comment**: User comments on articles
- **ShareCount**: Social media share tracking
- **Subscriber**: Newsletter email list

## Technology Stack

### Backend
- Django 5.2
- Django REST Framework
- SQLite/PostgreSQL
- Pillow (image processing)
- django-cors-headers

### Frontend
- React 18
- React Router v6
- Axios
- React Query
- Webpack 5
- Babel

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

### CORS Errors
Ensure Django settings include:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
```

### Module Not Found
```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend && npm install
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a pull request

## Scripts Reference

- `setup.sh` - Complete project setup
- `dev_server.sh` - Start both servers
- `build_frontend.sh` - Build React for production
- `migrate_postgres.sh` - Migrate to PostgreSQL
- `quick_migration.sh` - Quick database migration

## License
MIT

## Support
For questions or issues, please check the documentation in the `docs/` folder or contact the development team.

---

**Last Updated**: December 4, 2025  
**Version**: 1.0.0
