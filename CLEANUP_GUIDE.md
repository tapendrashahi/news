# Repository Cleanup Guide

## Overview
Since the project has been fully migrated to React for both frontend and admin panel, several legacy Django template files and old migration scripts can be safely removed.

---

## ✅ Safe to Delete

### 1. Django Templates (No Longer Used)
**Location:** `news/templates/`

All templates are replaced by React components:
```bash
rm -rf news/templates/news/
rm -rf news/templates/admin/
```

**Files removed:**
- `news/templates/news/home.html` → React `Home.jsx`
- `news/templates/news/news_detail.html` → React `NewsDetail.jsx`
- `news/templates/news/category.html` → React `Category.jsx`
- `news/templates/news/about.html` → React `About.jsx`
- `news/templates/news/search_results.html` → React `Search.jsx`
- `news/templates/news/privacy_policy.html` → React `PrivacyPolicy.jsx`
- `news/templates/news/terms_of_service.html` → React `TermsOfService.jsx`
- `news/templates/news/cookee.html` → React `CookiePolicy.jsx`
- `news/templates/news/editorial_guideline.html` → React `EditorialGuidelines.jsx`
- `news/templates/news/ethics_policy.html` → React `EthicsPolicy.jsx`
- `news/templates/news/base.html` → React `Layout.jsx`
- Admin templates → React Admin Panel

### 2. Static CSS Files (No Longer Used)
**Location:** `news/static/css/`

Replaced by React component CSS modules:
```bash
rm -rf news/static/
```

**Files removed:**
- `news/static/css/style.css` → React component CSS files

### 3. Django Template Views (No Longer Used)
**Location:** `news/views.py`

These view functions are replaced by React Router + REST API:
- `home()` → React `Home.jsx` + `/api/news/`
- `news_detail()` → React `NewsDetail.jsx` + `/api/news/{id}/`
- `category_page()` → React `Category.jsx` + `/api/news/?category=`
- `about()` → React `About.jsx` + `/api/team/`
- `search()` → React `Search.jsx` + `/api/news/?search=`
- Legal pages → React pages + JSON files

**Action:** Keep file but these functions can be removed (or keep for legacy support)

### 4. Old URL Patterns
**Location:** `news/urls.py`

These URLs are no longer needed (replaced by React Router):
```python
# Can be removed:
path('', views.home, name='home'),
path('category/<str:category>/', views.category_page, name='category'),
path('news/<int:pk>/', views.news_detail, name='news_detail'),
path('about/', views.about, name='about'),
path('search/', views.search, name='search'),
# ... legal pages
```

**Keep only:**
- API URLs (in `news/api_urls.py`)
- Admin URLs (in `news/admin_urls.py`)

### 5. Old Migration Scripts (Completed)
```bash
rm migrate_to_mongo.py
rm migrate_to_postgresql.py
rm migrate_postgres.sh
rm sync_sqlite_to_mongo.py
rm sync_to_mongo.py
rm quick_migration.sh
rm temp_sqlite_settings.py
```

### 6. Test/Debug Files
```bash
rm create_sample_jobs.py
rm test_admin_api.py
rm test_ads_api.py
rm fix_ad_date.py
rm test_jobs.sql
```

### 7. Backup Files
```bash
rm db.sqlite3.backup
rm sqlite_backup.json
```

### 8. Old Documentation (Consolidate)
```bash
rm CAREERS_IMPLEMENTATION.md
rm LEGAL_PAGES_IMPLEMENTATION_PLAN.md
rm POSTGRESQL_MIGRATION.md
```

### 9. Administration JSON Files (Already in Database)
```bash
rm -rf administration/
```

These are loaded into database, no longer needed as separate files.

---

## ⚠️ Keep (Still Used)

### Core Django Files
- `manage.py` - Django management
- `requirements.txt` - Python dependencies
- `gis/` - Django project settings
- `news/` - Django app (models, API, serializers)
  - Keep: `models.py`, `serializers.py`, `api.py`, `api_admin.py`, `admin.py`
  - Keep: `api_urls.py`, `admin_urls.py`
  - Keep: `migrations/`

### Frontend
- `frontend/` - Complete React application
- `build_frontend.sh` - Build script
- `dev_server.sh` - Development server script
- `setup.sh` - Setup script

### Database & Media
- `db.sqlite3` - Database (or keep your production DB)
- `media/` - Uploaded images

### Documentation
- `docs/` - Keep all documentation
- `README_REACT.md` - Main README
- `CHECKLIST.md` - Project checklist

### Configuration
- `.env` - Environment variables
- `.git/` - Git repository
- `.venv/` - Virtual environment (or regenerate)

---

## 🧹 Cleanup Script

Run this script to clean up safely:

```bash
#!/bin/bash
# cleanup_repo.sh

echo "🧹 Starting repository cleanup..."

# 1. Remove Django templates
echo "Removing Django templates..."
rm -rf news/templates/

# 2. Remove static files
echo "Removing static CSS..."
rm -rf news/static/

# 3. Remove migration scripts
echo "Removing old migration scripts..."
rm -f migrate_to_mongo.py
rm -f migrate_to_postgresql.py
rm -f migrate_postgres.sh
rm -f sync_sqlite_to_mongo.py
rm -f sync_to_mongo.py
rm -f quick_migration.sh
rm -f temp_sqlite_settings.py

# 4. Remove test files
echo "Removing test/debug files..."
rm -f create_sample_jobs.py
rm -f test_admin_api.py
rm -f test_ads_api.py
rm -f fix_ad_date.py
rm -f test_jobs.sql

# 5. Remove backups
echo "Removing backup files..."
rm -f db.sqlite3.backup
rm -f sqlite_backup.json

# 6. Remove old documentation
echo "Removing old documentation..."
rm -f CAREERS_IMPLEMENTATION.md
rm -f LEGAL_PAGES_IMPLEMENTATION_PLAN.md
rm -f POSTGRESQL_MIGRATION.md

# 7. Remove administration JSON folder
echo "Removing administration JSON files..."
rm -rf administration/

echo "✅ Cleanup complete!"
echo ""
echo "Removed:"
echo "  - Django templates"
echo "  - Static CSS files"
echo "  - Old migration scripts"
echo "  - Test/debug files"
echo "  - Backup files"
echo "  - Old documentation"
echo "  - Administration JSON files"
echo ""
echo "Repository is now cleaner! 🎉"
```

---

## 📊 Before & After

### Before Cleanup (~150+ files)
```
news/
├── templates/ (15+ template files) ❌
├── static/ (CSS files) ❌
├── views.py (template views) ⚠️
├── urls.py (template URLs) ⚠️
...

Root:
├── migrate_*.py (5 files) ❌
├── test_*.py (3 files) ❌
├── *_backup.* (2 files) ❌
├── administration/ ❌
```

### After Cleanup (~100 files)
```
news/
├── models.py ✅
├── serializers.py ✅
├── api.py ✅
├── api_admin.py ✅
├── api_urls.py ✅
├── admin_urls.py ✅
├── migrations/ ✅

Root:
├── frontend/ ✅
├── docs/ ✅
├── manage.py ✅
├── requirements.txt ✅
```

---

## 🔧 Update After Cleanup

### 1. Update `news/urls.py`
Since templates are removed, update to only serve API:

```python
from django.urls import path, include

app_name = 'news'

urlpatterns = [
    # API endpoints
    path('api/', include('news.api_urls')),
    
    # Admin endpoints
    path('admin/', include('news.admin_urls')),
]
```

### 2. Update `gis/urls.py`
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),  # This now only has API routes
]

# Serve media files in development
if settings.DEBUG:
    urlpatages += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 3. Update `news/views.py`
Remove or comment out all template view functions (keep only if you want legacy support).

---

## ✅ Verification Steps

After cleanup:

1. **Test API endpoints:**
   ```bash
   curl http://localhost:8000/api/news/
   curl http://localhost:8000/api/team/
   ```

2. **Test React frontend:**
   ```bash
   cd frontend
   npm start
   ```

3. **Test React admin:**
   ```bash
   # Navigate to http://localhost:3000/admin
   ```

4. **Check file count:**
   ```bash
   find . -type f | wc -l
   ```

---

## 💾 Backup Before Cleanup

**Create backup first:**
```bash
# Backup entire project
tar -czf news_backup_$(date +%Y%m%d).tar.gz \
  --exclude='.git' \
  --exclude='node_modules' \
  --exclude='.venv' \
  --exclude='__pycache__' \
  .

# Or just backup files to be deleted
mkdir -p ../news_deleted_files
cp -r news/templates ../news_deleted_files/
cp -r news/static ../news_deleted_files/
cp -r administration ../news_deleted_files/
```

---

## 📝 Summary

**Total files to remove:** ~50+ files and folders
**Disk space saved:** ~2-5 MB (more if templates had assets)
**Result:** Cleaner, more maintainable React-only codebase

**Safe to proceed:** Yes, all functionality is handled by React + REST API
