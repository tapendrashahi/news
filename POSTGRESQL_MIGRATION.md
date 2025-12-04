# PostgreSQL Migration Guide

## Step 1: Install PostgreSQL

### On Ubuntu/Debian:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### On macOS:
```bash
brew install postgresql
brew services start postgresql
```

### On Windows:
Download and install from: https://www.postgresql.org/download/windows/

## Step 2: Create PostgreSQL Database

Access PostgreSQL:
```bash
sudo -u postgres psql
```

Create database and user:
```sql
CREATE DATABASE news_db;
CREATE USER news_user WITH PASSWORD 'your_secure_password';
ALTER ROLE news_user SET client_encoding TO 'utf8';
ALTER ROLE news_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE news_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE news_db TO news_user;
\q
```

## Step 3: Update Django Settings

The settings.py has been updated. You need to change:
- `PASSWORD`: Set your PostgreSQL password
- `USER`: Use 'news_user' or 'postgres'

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'news_db',
        'USER': 'news_user',  # or 'postgres'
        'PASSWORD': 'your_secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Step 4: Backup SQLite Data (IMPORTANT!)

Before migrating, backup your SQLite database:
```bash
# Backup the database file
cp db.sqlite3 db.sqlite3.backup

# Export data to JSON
python manage.py dumpdata --natural-foreign --natural-primary --exclude=contenttypes --exclude=auth.permission --indent=2 > sqlite_backup.json
```

## Step 5: Run PostgreSQL Migrations

```bash
# Run migrations on PostgreSQL
python manage.py migrate
```

## Step 6: Create Superuser

```bash
python manage.py createsuperuser
```

## Step 7: Load Data from SQLite Backup

```bash
python manage.py loaddata sqlite_backup.json
```

## Step 8: Verify Migration

Start the server and check:
```bash
python manage.py runserver
```

Visit:
- Admin: http://localhost:8000/custom-admin/
- Website: http://localhost:8000/

## Troubleshooting

### Connection Error
If you get "connection refused":
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Start PostgreSQL
sudo systemctl start postgresql
```

### Authentication Failed
Check pg_hba.conf file:
```bash
sudo nano /etc/postgresql/*/main/pg_hba.conf
```

Change authentication method to 'md5':
```
local   all             all                                     md5
host    all             all             127.0.0.1/32            md5
```

Restart PostgreSQL:
```bash
sudo systemctl restart postgresql
```

### Permission Denied
Grant privileges:
```bash
sudo -u postgres psql
GRANT ALL PRIVILEGES ON DATABASE news_db TO news_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO news_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO news_user;
```

## Rollback (If Needed)

To go back to SQLite:
1. Restore settings.py to use SQLite
2. Restore db.sqlite3.backup:
```bash
cp db.sqlite3.backup db.sqlite3
```

## Quick Migration Commands

```bash
# 1. Backup SQLite data
python manage.py dumpdata --exclude=contenttypes --exclude=auth.permission --indent=2 > sqlite_backup.json

# 2. Update settings.py with PostgreSQL credentials

# 3. Run migrations
python manage.py migrate

# 4. Create superuser
python manage.py createsuperuser

# 5. Load data
python manage.py loaddata sqlite_backup.json

# 6. Test
python manage.py runserver
```

## Performance Tips

After migration, analyze tables for better performance:
```sql
-- Connect to database
psql -U news_user -d news_db

-- Analyze tables
ANALYZE;

-- Vacuum tables
VACUUM ANALYZE;
```
