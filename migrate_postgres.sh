#!/bin/bash

# PostgreSQL Migration Script for News Project
# This script automates the migration from SQLite to PostgreSQL

set -e  # Exit on any error

echo "╔══════════════════════════════════════════════════════════╗"
echo "║     SQLite to PostgreSQL Migration Script               ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
DB_NAME="news_db"
DB_USER="news_user"
BACKUP_FILE="sqlite_backup.json"
SQLITE_BACKUP="db.sqlite3.backup"

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo -e "${RED}❌ PostgreSQL is not installed!${NC}"
    echo "Please install PostgreSQL first:"
    echo "  Ubuntu/Debian: sudo apt install postgresql postgresql-contrib"
    echo "  macOS: brew install postgresql"
    exit 1
fi

echo -e "${GREEN}✅ PostgreSQL is installed${NC}"

# Check if PostgreSQL is running
if ! pg_isready &> /dev/null; then
    echo -e "${YELLOW}⚠️  PostgreSQL is not running. Starting...${NC}"
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo systemctl start postgresql
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew services start postgresql
    fi
fi

echo -e "${GREEN}✅ PostgreSQL is running${NC}"

# Ask for database password
echo ""
read -sp "Enter password for PostgreSQL user '$DB_USER': " DB_PASSWORD
echo ""

# Step 1: Backup SQLite data
echo ""
echo "📦 Step 1: Backing up SQLite data..."
if [ -f "db.sqlite3" ]; then
    cp db.sqlite3 "$SQLITE_BACKUP"
    echo -e "${GREEN}✅ SQLite database backed up to $SQLITE_BACKUP${NC}"
    
    # Export data
    source .venv/bin/activate 2>/dev/null || true
    python manage.py dumpdata --natural-foreign --natural-primary \
        --exclude=contenttypes --exclude=auth.permission \
        --indent=2 > "$BACKUP_FILE"
    echo -e "${GREEN}✅ Data exported to $BACKUP_FILE${NC}"
else
    echo -e "${YELLOW}⚠️  No SQLite database found${NC}"
fi

# Step 2: Create PostgreSQL database
echo ""
echo "🗄️  Step 2: Setting up PostgreSQL database..."
sudo -u postgres psql << EOF
DROP DATABASE IF EXISTS $DB_NAME;
DROP USER IF EXISTS $DB_USER;
CREATE DATABASE $DB_NAME;
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
ALTER ROLE $DB_USER SET client_encoding TO 'utf8';
ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';
ALTER ROLE $DB_USER SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
\c $DB_NAME
GRANT ALL ON SCHEMA public TO $DB_USER;
EOF

echo -e "${GREEN}✅ PostgreSQL database created${NC}"

# Step 3: Update settings.py
echo ""
echo "⚙️  Step 3: Updating settings.py..."
cat > gis/settings_postgres.py << EOF
# PostgreSQL Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '$DB_NAME',
        'USER': '$DB_USER',
        'PASSWORD': '$DB_PASSWORD',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
EOF

# Backup original settings
cp gis/settings.py gis/settings_sqlite_backup.py

# Update database configuration in settings.py
python << PYTHON_SCRIPT
import re

with open('gis/settings.py', 'r') as f:
    content = f.read()

# Replace DATABASES configuration
db_config = """DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '$DB_NAME',
        'USER': '$DB_USER',
        'PASSWORD': '$DB_PASSWORD',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}"""

content = re.sub(
    r"DATABASES\s*=\s*{[^}]*'default'[^}]*{[^}]*}[^}]*}",
    db_config,
    content,
    flags=re.DOTALL
)

with open('gis/settings.py', 'w') as f:
    f.write(content)
PYTHON_SCRIPT

echo -e "${GREEN}✅ Settings updated (backup saved to settings_sqlite_backup.py)${NC}"

# Step 4: Run migrations
echo ""
echo "🔄 Step 4: Running migrations..."
source .venv/bin/activate 2>/dev/null || true
python manage.py migrate

echo -e "${GREEN}✅ Migrations completed${NC}"

# Step 5: Load data
if [ -f "$BACKUP_FILE" ]; then
    echo ""
    echo "📥 Step 5: Loading data from backup..."
    python manage.py loaddata "$BACKUP_FILE"
    echo -e "${GREEN}✅ Data loaded successfully${NC}"
else
    echo -e "${YELLOW}⚠️  No backup file found, skipping data import${NC}"
    echo ""
    echo "Creating superuser..."
    python manage.py createsuperuser
fi

# Step 6: Verify
echo ""
echo "✨ Migration complete!"
echo ""
echo "Next steps:"
echo "1. Test your application: python manage.py runserver"
echo "2. Visit: http://localhost:8000/custom-admin/"
echo ""
echo "Backup files:"
echo "  - SQLite backup: $SQLITE_BACKUP"
echo "  - Data backup: $BACKUP_FILE"
echo "  - Settings backup: gis/settings_sqlite_backup.py"
echo ""
echo -e "${GREEN}✅ All done!${NC}"
