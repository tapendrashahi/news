# Quick Start Guide - React Integration

## 🚀 Get Started in 5 Minutes

### Step 1: Run Setup Script
```bash
chmod +x setup.sh
./setup.sh
```

This installs all dependencies and sets up the database.

### Step 2: Start Development Servers

**Option A - Automated (Recommended)**
```bash
./dev_server.sh
```

**Option B - Manual**

Terminal 1:
```bash
source venv/bin/activate
python manage.py runserver
```

Terminal 2:
```bash
cd frontend
npm start
```

### Step 3: Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api
- Admin Panel: http://localhost:8000/admin

## 📁 Project Overview

```
news/
├── frontend/          # React application
│   ├── src/
│   │   ├── components/  # UI components
│   │   ├── pages/       # Page views
│   │   ├── services/    # API calls
│   │   └── App.jsx
│   └── package.json
│
├── gis/              # Django settings
├── news/             # Django app
├── docs/             # Documentation
└── manage.py
```

## 🔧 Common Tasks

### Install New Python Package
```bash
source venv/bin/activate
pip install package-name
pip freeze > requirements.txt
```

### Install New npm Package
```bash
cd frontend
npm install package-name
```

### Create Django API Endpoint
1. Add serializer in `news/serializers.py`
2. Add view in `news/api.py`
3. Add URL in `news/api_urls.py`

### Create React Component
1. Create file in `frontend/src/components/`
2. Import and use in pages
3. Add routing if needed in `routes.jsx`

## 📚 Documentation

Detailed guides available in `docs/`:
- `react_integration_plan.md` - Complete architecture plan
- `frontend_structure.md` - React folder structure
- `api_documentation.md` - API endpoints reference
- `setup_guide.md` - Detailed setup instructions

## 🎯 Next Steps

### 1. Set Up Django REST API
Create `news/serializers.py` and `news/api_urls.py`

### 2. Build React Components
Start with NewsCard, NewsList, Header, Footer

### 3. Connect Frontend to Backend
Update API services to fetch real data

### 4. Add Features
- Search functionality
- Category filters
- Comments
- Newsletter

## 🐛 Troubleshooting

**Port already in use:**
```bash
lsof -ti:8000 | xargs kill -9  # Django
lsof -ti:3000 | xargs kill -9  # React
```

**CORS errors:**
Check `CORS_ALLOWED_ORIGINS` in `gis/settings.py`

**Module not found:**
```bash
pip install -r requirements.txt    # Backend
cd frontend && npm install         # Frontend
```

## ✅ Checklist

- [ ] Run `./setup.sh`
- [ ] Create superuser for admin
- [ ] Configure `.env` files
- [ ] Start both servers
- [ ] Access frontend at localhost:3000
- [ ] Verify API at localhost:8000/api
- [ ] Check admin panel
- [ ] Read documentation in `docs/`

## 🎨 Development Tips

1. **Hot Reload**: React auto-reloads on save
2. **API Testing**: Use browser or Postman
3. **Debug**: React DevTools + Django Debug Toolbar
4. **Code Quality**: Run lint before commits
5. **Git**: Don't commit .env files

## 📞 Need Help?

1. Check `docs/` folder for detailed guides
2. Review `README_REACT.md` for complete overview
3. Check Django/React official documentation

---

Happy Coding! 🎉
