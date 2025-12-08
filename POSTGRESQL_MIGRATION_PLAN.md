# PostgreSQL Migration Plan

**Date**: December 8, 2025  
**Current Status**: SQLite → PostgreSQL (Partially Migrated)  
**Issue**: PostgreSQL database is missing recent migrations (Jobs & Advertisements)

---

## 📊 Current State Analysis

### SQLite Database (Current Active)
✅ **All migrations applied** (13 total):
- 0001_initial → 0011_subscriber (Base migrations)
- **0012_jobopening_jobapplication** ✅ (Jobs feature - NEW)
- **0013_advertisement** ✅ (Advertisement system - NEW)

### PostgreSQL Database (Existing but Outdated)
⚠️ **Only 11 migrations applied**:
- 0001_initial → 0011_subscriber ✅
- **0012_jobopening_jobapplication** ❌ MISSING
- **0013_advertisement** ❌ MISSING

### Missing Tables in PostgreSQL
- `news_jobopening`
- `news_jobapplication`
- `news_advertisement`

---

## 🎯 Migration Strategy

### Option 1: Apply Missing Migrations (Recommended - Preserves Old Data)
Keep existing PostgreSQL data and apply only the new migrations.

**Pros:**
- Preserves any old data in PostgreSQL
- Faster migration
- Less risk

**Cons:**
- Won't sync recent SQLite data changes

### Option 2: Fresh Migration with Data Transfer (Complete Sync)
Migrate all data from SQLite to PostgreSQL, including recent changes.

**Pros:**
- Complete data sync
- All recent data (news, comments, jobs, ads) transferred
- Clean state

**Cons:**
- Takes longer
- Need to backup first

---

## ✅ Recommended Approach: Option 2 (Complete Migration)

Since you've been actively working in SQLite for 2-3 days with new data, we should transfer everything.

---

## 📋 Step-by-Step Migration Plan

### Phase 1: Preparation (5 minutes)

#### 1. Backup Current Databases
```bash
# Backup SQLite (current working database)
cp db.sqlite3 db.sqlite3.backup_$(date +%Y%m%d_%H%M%S)

# Backup PostgreSQL (optional, if has important data)
PGPASSWORD='Tapendra@1' pg_dump -U news_user -h localhost news > postgres_backup_$(date +%Y%m%d_%H%M%S).sql
```

#### 2. Install Required Packages
```bash
# Ensure psycopg2 is installed (PostgreSQL adapter)
pip install psycopg2-binary
```

#### 3. Verify PostgreSQL Connection
```bash
PGPASSWORD='Tapendra@1' psql -U news_user -h localhost -d news -c "SELECT version();"
```

---

### Phase 2: Database Setup (2 minutes)

#### 1. Drop and Recreate PostgreSQL Database (Clean Slate)
```bash
# Connect as postgres superuser
sudo -u postgres psql << 'EOF'
-- Drop existing database
DROP DATABASE IF EXISTS news;

-- Recreate database
CREATE DATABASE news
    WITH OWNER = news_user
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TEMPLATE = template0;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE news TO news_user;
EOF
```

#### 2. Update Django Settings
```bash
# Set environment variable to use PostgreSQL
export USE_SQLITE=False

# Or update .env file
echo "USE_SQLITE=False" >> .env
```

---

### Phase 3: Apply Migrations (2 minutes)

#### 1. Run All Migrations on PostgreSQL
```bash
# This will create all tables including jobs and advertisements
python manage.py migrate
```

#### 2. Verify Migrations
```bash
# Check all migrations are applied
python manage.py showmigrations news

# Should show all 13 migrations with [X]
```

#### 3. Verify Tables
```bash
PGPASSWORD='Tapendra@1' psql -U news_user -h localhost -d news -c "\dt"

# Should include:
# - news_jobopening
# - news_jobapplication  
# - news_advertisement
```

---

### Phase 4: Data Migration (5-10 minutes)

#### 1. Export Data from SQLite
```bash
# Using Django's dumpdata
python manage.py dumpdata \
    --database=default \
    --natural-foreign \
    --natural-primary \
    --exclude=contenttypes \
    --exclude=auth.permission \
    --indent=2 \
    > sqlite_data_export.json
```

#### 2. Switch to PostgreSQL
```bash
# Update .env
echo "USE_SQLITE=False" > .env.tmp && mv .env.tmp .env

# Or set environment variable
export USE_SQLITE=False
```

#### 3. Import Data to PostgreSQL
```bash
# Load data into PostgreSQL
python manage.py loaddata sqlite_data_export.json
```

#### 4. Verify Data Transfer
```bash
# Check record counts
PGPASSWORD='Tapendra@1' psql -U news_user -h localhost -d news << 'EOF'
SELECT 'News' as table_name, COUNT(*) FROM news_news
UNION ALL
SELECT 'Team Members', COUNT(*) FROM news_teammember
UNION ALL
SELECT 'Comments', COUNT(*) FROM news_comment
UNION ALL
SELECT 'Subscribers', COUNT(*) FROM news_subscriber
UNION ALL
SELECT 'Jobs', COUNT(*) FROM news_jobopening
UNION ALL
SELECT 'Applications', COUNT(*) FROM news_jobapplication
UNION ALL
SELECT 'Advertisements', COUNT(*) FROM news_advertisement;
EOF
```

---

### Phase 5: Create Superuser (1 minute)

Since we recreated the database, create a new superuser:

```bash
python manage.py createsuperuser
```

---

### Phase 6: Testing (5 minutes)

#### 1. Start Django Server
```bash
python manage.py runserver
```

#### 2. Test API Endpoints
```bash
# Test news
curl http://localhost:8000/api/news/

# Test team
curl http://localhost:8000/api/team/

# Test jobs
curl http://localhost:8000/api/jobs/

# Test advertisements
curl http://localhost:8000/api/advertisements/
```

#### 3. Test Admin Panel
- Visit: http://localhost:3000/admin
- Login with new superuser
- Check all pages load
- Verify data is visible

#### 4. Test Frontend
- Visit: http://localhost:3000
- Check news articles display
- Check advertisements display
- Test job applications
- Submit a comment

---

## 🔧 Alternative: Quick Migration Script

I'll create an automated script that does all of this:

```bash
./migrate_to_postgresql.sh
```

The script will:
1. ✅ Backup SQLite database
2. ✅ Drop & recreate PostgreSQL database
3. ✅ Apply all migrations
4. ✅ Export data from SQLite
5. ✅ Import data to PostgreSQL
6. ✅ Verify migration
7. ✅ Update settings

---

## 📊 Migration Checklist

**Before Migration:**
- [ ] Backup SQLite database
- [ ] Verify PostgreSQL is running
- [ ] Test PostgreSQL connection
- [ ] Install psycopg2-binary
- [ ] Stop Django server

**During Migration:**
- [ ] Drop and recreate PostgreSQL database
- [ ] Apply all migrations (13 total)
- [ ] Export SQLite data
- [ ] Import to PostgreSQL
- [ ] Create superuser

**After Migration:**
- [ ] Verify all tables exist
- [ ] Check data counts match
- [ ] Test API endpoints
- [ ] Test admin panel
- [ ] Test frontend
- [ ] Update .env to USE_SQLITE=False

**Verification:**
- [ ] All 13 migrations applied
- [ ] All tables created (15+ tables)
- [ ] Data transferred correctly
- [ ] Images accessible (check MEDIA_ROOT)
- [ ] Admin authentication works
- [ ] Frontend loads data

---

## ⚠️ Important Notes

### 1. Media Files
Media files (images) are stored in `media/` folder, not in database. They will work with PostgreSQL without changes.

### 2. Settings Configuration
Your `gis/settings.py` already has PostgreSQL configuration. Just need to set:
```bash
USE_SQLITE=False
```

### 3. Connection String
Current PostgreSQL credentials from `.env`:
```
Host: localhost
Port: 5432
Database: news
User: news_user
Password: Tapendra@1
```

### 4. Performance
PostgreSQL will be faster for:
- Complex queries
- Multiple concurrent users
- Production deployment
- Data integrity

---

## 🚀 Quick Start

### Automated Migration
```bash
# Run the migration script I'll create
./migrate_to_postgresql.sh
```

### Manual Migration
```bash
# 1. Backup
cp db.sqlite3 db.sqlite3.backup

# 2. Export SQLite data
python manage.py dumpdata --natural-foreign --natural-primary \
    --exclude=contenttypes --exclude=auth.permission \
    --indent=2 > sqlite_export.json

# 3. Recreate PostgreSQL database
sudo -u postgres psql -c "DROP DATABASE IF EXISTS news;"
sudo -u postgres psql -c "CREATE DATABASE news OWNER news_user;"

# 4. Set to use PostgreSQL
export USE_SQLITE=False

# 5. Apply migrations
python manage.py migrate

# 6. Load data
python manage.py loaddata sqlite_export.json

# 7. Create superuser
python manage.py createsuperuser

# 8. Start server
python manage.py runserver
```

---

## 📈 Expected Results

### Before Migration (SQLite)
- Database: `db.sqlite3` (size: ~500KB - 2MB)
- Tables: 18 tables
- Migrations: 13 applied
- Data: All current data

### After Migration (PostgreSQL)
- Database: `news` in PostgreSQL
- Tables: 18 tables (same structure)
- Migrations: 13 applied
- Data: All data transferred
- Performance: Improved for concurrent access

---

## 🆘 Troubleshooting

### Issue 1: "psycopg2 not found"
```bash
pip install psycopg2-binary
```

### Issue 2: "Permission denied"
```bash
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE news TO news_user;"
```

### Issue 3: "Data import fails"
```bash
# Try importing in chunks
python manage.py loaddata sqlite_export.json --verbosity=2
```

### Issue 4: "Duplicate key error"
```bash
# Clear PostgreSQL and retry
python manage.py flush --database=default
python manage.py loaddata sqlite_export.json
```

---

## ✅ Success Criteria

Migration is successful when:
1. ✅ All 13 migrations applied to PostgreSQL
2. ✅ All tables created (news_jobopening, news_jobapplication, news_advertisement exist)
3. ✅ Data counts match between SQLite export and PostgreSQL
4. ✅ Admin panel loads and shows data
5. ✅ Frontend displays news, jobs, advertisements
6. ✅ No errors in Django logs
7. ✅ Images load correctly

---

**Ready to proceed?** I can create the automated migration script for you!
