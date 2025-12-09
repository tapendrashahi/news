# AI Analitica News Portal

A modern, full-stack news portal built with **Django REST Framework** and **React**, featuring a complete admin panel, advertisement system, job portal, and content management.

![React](https://img.shields.io/badge/React-18.2-blue)
![Django](https://img.shields.io/badge/Django-4.x-green)
![REST API](https://img.shields.io/badge/REST-API-orange)

---

## 🚀 Features

### Public Website
- 📰 **News Articles** - Browse, search, and filter news by category
- 🔍 **Advanced Search** - Full-text search across articles
- 💬 **Comments System** - User engagement with moderation
- 📧 **Newsletter** - Email subscription management
- 👥 **Team Page** - Meet the editorial team
- 💼 **Careers Portal** - Job listings and application system
- 📢 **Advertisement System** - With impression/click tracking
- 📱 **Mobile Responsive** - Optimized for all devices
- ⚡ **Fast & Modern** - React SPA with optimized performance

### Admin Panel
- 🔐 **Secure Authentication** - Session-based admin access
- 📝 **News Management** - Create, edit, delete articles with rich editor
- 👥 **Team Management** - Manage team members and profiles
- 💬 **Comment Moderation** - Approve, reject, or delete comments
- 📊 **Analytics Dashboard** - View statistics and insights
- 👤 **Subscriber Management** - View and manage newsletter subscribers
- 📢 **Advertisement Management** - Create and track ad campaigns
- 💼 **Job Management** - Post jobs and review applications
- 📈 **Reports** - Comprehensive analytics and reporting

### Advertisement System
- 🎯 **Position-based Display** - Sidebar, header, footer, inline
- 📊 **Tracking & Analytics** - Impressions, clicks, CTR
- 📅 **Scheduling** - Date range scheduling for campaigns
- 🔄 **Auto-rotation** - Multiple ads rotate automatically
- 📈 **Stats Dashboard** - Real-time performance metrics

---

## 🛠️ Tech Stack

### Backend
- **Django 4.x** - Web framework
- **Django REST Framework** - API development
- **SQLite** - Database (easily upgradable to PostgreSQL)
- **Pillow** - Image processing

### Frontend
- **React 18** - UI library
- **React Router v6** - Client-side routing
- **React Query (TanStack Query)** - Data fetching & caching
- **Axios** - HTTP client
- **CSS3** - Styling with CSS variables

### Development Tools
- **Webpack 5** - Module bundler
- **Babel** - JavaScript transpiler
- **ESLint** - Code linting
- **Prettier** - Code formatting

---

## 📋 Prerequisites

- **Python** 3.8+ with pip
- **Node.js** 16+ with npm
- **Git** (for version control)

---

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/tapendrashahi/news.git
cd news
```

### 2. Run Setup Script
```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Create Python virtual environment
- Install backend dependencies
- Install frontend dependencies
- Run database migrations
- Create a superuser

### 3. Start Development Servers
```bash
chmod +x dev_server.sh
./dev_server.sh
```

This starts both Django (port 8000) and React (port 3000) servers.

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Admin Panel**: http://localhost:3000/admin
- **Django Admin**: http://localhost:8000/admin
- **API**: http://localhost:8000/api/

---

## 📖 Manual Setup

### Backend Setup

1. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run migrations**
```bash
python manage.py migrate
```

4. **Create superuser**
```bash
python manage.py createsuperuser
```

5. **Start Django server**
```bash
python manage.py runserver
```

### Frontend Setup

1. **Navigate to frontend**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Create environment file**
```bash
cp .env.example .env
```

4. **Start development server**
```bash
npm start
```

---

## 📁 Project Structure

```
news/
├── backend/
│   ├── ai_analitica/           # Django project settings
│   │   ├── settings.py        # Main settings
│   │   ├── urls.py            # Root URL configuration
│   │   └── wsgi.py            # WSGI configuration
│   │
│   ├── news/                   # Main Django app
│   │   ├── models.py          # Database models
│   │   ├── serializers.py     # DRF serializers
│   │   ├── api.py             # Public API views
│   │   ├── api_admin.py       # Admin API views
│   │   ├── api_urls.py        # API URL patterns
│   │   ├── admin_urls.py      # Admin URL patterns
│   │   ├── permissions.py     # Custom permissions
│   │   └── migrations/        # Database migrations
│   │
│   ├── media/                  # User uploaded files
│   │   ├── news_images/       # Article images
│   │   ├── team_photos/       # Team member photos
│   │   └── advertisements/    # Ad images
│   │
│   ├── manage.py              # Django management script
│   └── requirements.txt       # Python dependencies
│
├── frontend/                   # React application
│   ├── src/
│   │   ├── components/        # Reusable components
│   │   │   ├── layout/       # Layout components
│   │   │   └── Advertisement.jsx
│   │   │
│   │   ├── pages/            # Page components
│   │   │   ├── Home.jsx
│   │   │   ├── NewsDetail.jsx
│   │   │   ├── Category.jsx
│   │   │   ├── Search.jsx
│   │   │   ├── About.jsx
│   │   │   ├── Team.jsx
│   │   │   ├── Careers.jsx
│   │   │   └── ... (legal pages)
│   │   │
│   │   ├── admin/            # Admin panel
│   │   │   ├── pages/        # Admin pages
│   │   │   ├── components/   # Admin components
│   │   │   ├── services/     # Admin services
│   │   │   └── context/      # Admin context
│   │   │
│   │   ├── services/         # API services
│   │   │   ├── api.js
│   │   │   ├── newsService.js
│   │   │   ├── advertisementService.js
│   │   │   └── ...
│   │   │
│   │   ├── hooks/            # Custom React hooks
│   │   ├── styles/           # Global styles
│   │   ├── App.jsx           # Root component
│   │   ├── routes.jsx        # Route definitions
│   │   └── index.jsx         # Entry point
│   │
│   ├── public/               # Static files
│   ├── config/               # Webpack configuration
│   ├── package.json          # Node dependencies
│   └── .env                  # Environment variables
│
├── docs/                      # Documentation
│   ├── api_documentation.md
│   ├── setup_guide.md
│   ├── quick_start.md
│   └── ...
│
├── build_frontend.sh         # Production build script
├── dev_server.sh             # Development server script
├── setup.sh                  # Initial setup script
├── cleanup_repo.sh           # Cleanup script
├── CLEANUP_GUIDE.md          # Cleanup documentation
└── README.md                 # This file
```

---

## 🔌 API Endpoints

### Public API

#### News
- `GET /api/news/` - List all news articles
- `GET /api/news/{id}/` - Get news detail
- `GET /api/news/?category={category}` - Filter by category
- `GET /api/news/?search={query}` - Search articles
- `POST /api/news/{id}/increment_views/` - Track article view

#### Team
- `GET /api/team/` - List team members

#### Comments
- `GET /api/comments/` - List comments
- `POST /api/comments/` - Add comment
- `GET /api/news/{id}/comments/` - Get comments for article

#### Advertisements
- `GET /api/advertisements/` - Get active ads
- `GET /api/advertisements/?position={position}` - Filter by position
- `POST /api/advertisements/{id}/track_impression/` - Track impression
- `POST /api/advertisements/{id}/track_click/` - Track click

#### Jobs
- `GET /api/jobs/` - List active job openings
- `GET /api/jobs/{id}/` - Get job details
- `POST /api/jobs/{id}/apply/` - Submit application

#### Subscribers
- `POST /api/subscribe/` - Subscribe to newsletter

### Admin API (Authentication Required)

#### News Management
- `GET /api/admin/news/` - List all news (admin)
- `POST /api/admin/news/` - Create news article
- `PUT /api/admin/news/{id}/` - Update article
- `DELETE /api/admin/news/{id}/` - Delete article

#### Team Management
- `GET /api/admin/team/` - List team members
- `POST /api/admin/team/` - Add team member
- `PUT /api/admin/team/{id}/` - Update member
- `DELETE /api/admin/team/{id}/` - Delete member

#### Advertisement Management
- `GET /api/admin/advertisements/` - List ads with stats
- `POST /api/admin/advertisements/` - Create ad
- `PUT /api/admin/advertisements/{id}/` - Update ad
- `DELETE /api/admin/advertisements/{id}/` - Delete ad
- `POST /api/admin/advertisements/{id}/toggle/` - Toggle active status
- `GET /api/admin/advertisements/stats/` - Get statistics

#### Comment Moderation
- `GET /api/admin/comments/` - List all comments
- `POST /api/admin/comments/{id}/approve/` - Approve comment
- `POST /api/admin/comments/{id}/reject/` - Reject comment
- `DELETE /api/admin/comments/{id}/` - Delete comment

#### Analytics
- `GET /api/admin/reports/stats/` - Get dashboard statistics
- `GET /api/admin/reports/popular-news/` - Popular articles
- `GET /api/admin/reports/category-distribution/` - Category stats

---

## 🎨 Features in Detail

### News Management
- Rich text editor for content
- Image upload with preview
- Category selection
- Tags and metadata
- Publication status (draft/published)
- Author attribution
- View counting
- Related articles

### Comment System
- User name and email collection
- Comment threading (ready for implementation)
- Moderation workflow (pending/approved/rejected)
- Admin approval required

### Advertisement System
- **Positions**: Sidebar, Header, Footer, Inline
- **Sizes**: Standard IAB sizes (300x250, 728x90, etc.)
- **Tracking**: Automatic impression and click tracking
- **Analytics**: CTR calculation, performance metrics
- **Scheduling**: Start and end dates
- **Display**: Auto-rotation for multiple ads

### Job Portal
- Job listing with details
- Application form with resume upload
- Application status tracking
- Admin review interface

---

## 🧹 Cleanup Legacy Files

The repository has been migrated from Django templates to React. To remove old template files:

```bash
./cleanup_repo.sh
```

See `CLEANUP_GUIDE.md` for details on what gets removed.

---

## 🚀 Production Deployment

### Build Frontend
```bash
./build_frontend.sh
```

This creates an optimized production build in `frontend/build/`.

### Django Production Settings

1. Update `ai_analitica/settings.py`:
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']

# Serve React build
STATICFILES_DIRS = [
    BASE_DIR / 'frontend/build/static',
]

TEMPLATES[0]['DIRS'] = [BASE_DIR / 'frontend/build']
```

2. Collect static files:
```bash
python manage.py collectstatic
```

3. Use production server (Gunicorn):
```bash
pip install gunicorn
gunicorn ai_analitica.wsgi:application
```

### Environment Variables

Create `.env` file:
```env
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=your-database-url
ALLOWED_HOSTS=yourdomain.com
```

---

## 🧪 Testing

### Backend Tests
```bash
python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm test
```

---

## 📚 Documentation

- [API Documentation](docs/api_documentation.md)
- [Setup Guide](docs/setup_guide.md)
- [Quick Start](docs/quick_start.md)
- [Architecture](docs/architecture_diagram.md)
- [Frontend Structure](docs/frontend_structure.md)
- [Cleanup Guide](CLEANUP_GUIDE.md)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License.

---

## 👥 Team

Built by the AI Analitica team.

---

## 🆘 Support

For issues and questions:
- Create an issue on GitHub
- Check documentation in `docs/` folder
- Review `CLEANUP_GUIDE.md` for cleanup questions

---

## 🎉 Acknowledgments

- Django REST Framework team
- React team
- All contributors

---

**Last Updated**: December 8, 2025
**Version**: 2.0.0 (React Migration Complete)
