# GIS Project Structure

This document provides an overview of the project's directory structure and file organization.

## Root Directory

```
gis/
├── docs/                       # Documentation files
│   └── project_structure.md    # This file
├── gis/                        # Main Django project configuration
│   ├── __init__.py
│   ├── __pycache__/           # Python bytecode cache
│   ├── asgi.py                # ASGI configuration for async support
│   ├── settings.py            # Django project settings
│   ├── urls.py                # Main URL routing configuration
│   └── wsgi.py                # WSGI configuration for deployment
├── news/                       # News Django application
│   ├── __pycache__/           # Python bytecode cache
│   ├── migrations/            # Database migrations
│   │   ├── __pycache__/
│   │   ├── 0001_initial.py    # Initial migration
│   │   └── __init__.py
│   ├── __init__.py            # Python package marker
│   ├── admin.py               # Django admin panel configuration
│   ├── asgi.py                # ASGI configuration
│   ├── manage.py              # Django management script
│   ├── models.py              # Database models (News model)
│   ├── settings.py            # App-specific settings
│   ├── urls.py                # URL routing for news app
│   └── wsgi.py                # WSGI configuration
├── venv/                       # Python virtual environment
│   ├── Include/
│   ├── Lib/
│   │   └── site-packages/     # Third-party packages
│   │       ├── asgiref/       # ASGI reference implementation
│   │       ├── django/        # Django framework
│   │       ├── pip/           # Package installer
│   │       ├── sqlparse/      # SQL parser
│   │       └── tzdata/        # Timezone data
│   ├── Scripts/               # Virtual environment executables
│   └── pyvenv.cfg             # Virtual environment configuration
├── db.sqlite3                  # SQLite database file
├── manage.py                   # Django management script (root)
└── requirements.txt            # Python dependencies list
```

## Directory Descriptions

### `/gis` - Main Project Configuration
The main Django project configuration directory containing:
- **settings.py**: Project-wide settings (database, installed apps, middleware, static files, etc.)
- **urls.py**: Root URL configuration that routes to different apps
- **wsgi.py**: WSGI configuration for production deployment
- **asgi.py**: ASGI configuration for asynchronous support

### `/news` - News Application
A Django application for managing news content. Contains:
- **models.py**: Database models (includes the News model)
- **admin.py**: Django admin panel configuration to manage News objects
- **migrations/**: Database migration files for schema changes
- **settings.py**: Application-specific configuration settings
- **urls.py**: URL routing specific to the news app
- **asgi.py** & **wsgi.py**: Server gateway interface configurations
- **manage.py**: Django management script for the news app

### `/docs` - Documentation
Project documentation including:
- **project_structure.md**: This file - comprehensive project structure overview

### `/venv` - Virtual Environment
Python virtual environment containing:
- All installed dependencies from requirements.txt
- Isolated Python packages including Django, asgiref, sqlparse, and tzdata
- Platform-specific executables in Scripts/

## Key Files

| File | Description |
|------|-------------|
| `manage.py` | Django command-line utility for administrative tasks (migrations, runserver, etc.) |
| `db.sqlite3` | SQLite database file storing all application data |
| `requirements.txt` | Complete list of Python package dependencies with versions |
| `gis/settings.py` | Main Django configuration (database, apps, middleware, templates, etc.) |
| `gis/urls.py` | Root URL routing configuration |
| `news/models.py` | Data models for the news application (News model) |
| `news/admin.py` | Admin interface configuration for managing News objects |
| `news/migrations/0001_initial.py` | Initial database migration for News model |

## Technology Stack

Based on the project structure, this appears to be a **Django** web application using:
- Python (Django framework)
- SQLite database
- ASGI/WSGI for web server interfaces

## Notes

- The project uses a virtual environment (`venv/`) for isolated dependency management
- SQLite is used as the database (suitable for development; consider PostgreSQL/MySQL for production)
- The News model is registered in the Django admin panel for easy content management
- `__pycache__/` directories contain Python bytecode (should be excluded from version control)
- The project structure follows Django best practices with proper app organization

## Getting Started

To work with this project:

1. Activate the virtual environment:
   ```bash
   venv\Scripts\activate  # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Start the development server:
   ```bash
   python manage.py runserver
   ```

---

*Last updated: 2025-11-22*
