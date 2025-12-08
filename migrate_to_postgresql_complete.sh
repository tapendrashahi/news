#!/bin/bash
# PostgreSQL Migration Script
# Migrates data from SQLite to PostgreSQL including new tables (Jobs & Advertisements)

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     PostgreSQL Migration Script                            ║"
echo "║     SQLite → PostgreSQL (Complete Data Transfer)           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Configuration from .env
PGHOST="${PGHOST:-localhost}"
PGPORT="${PGPORT:-5432}"
PGDATABASE="${PGDATABASE:-news}"
PGUSER="${PGUSER:-news_user}"
PGPASSWORD="${PGPASSWORD:-Tapendra@1}"

# Export for psql commands
export PGPASSWORD

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_step() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}$1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check if SQLite database exists
if [ ! -f "db.sqlite3" ]; then
    print_error "SQLite database (db.sqlite3) not found!"
    exit 1
fi

echo "Current Configuration:"
echo "  SQLite Database: db.sqlite3"
echo "  PostgreSQL Host: $PGHOST"
echo "  PostgreSQL Port: $PGPORT"
echo "  PostgreSQL Database: $PGDATABASE"
echo "  PostgreSQL User: $PGUSER"
echo ""

read -p "Continue with migration? This will REPLACE all PostgreSQL data! (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Migration cancelled."
    exit 0
fi

# Step 1: Backup SQLite
print_step "Step 1: Backup SQLite Database"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SQLITE_BACKUP="db.sqlite3.backup_${TIMESTAMP}"
cp db.sqlite3 "$SQLITE_BACKUP"
print_success "SQLite backed up to: $SQLITE_BACKUP"

# Step 2: Test PostgreSQL Connection
print_step "Step 2: Testing PostgreSQL Connection"
if psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d postgres -c "SELECT version();" > /dev/null 2>&1; then
    print_success "PostgreSQL connection successful"
else
    print_error "Cannot connect to PostgreSQL!"
    print_warning "Please check your PostgreSQL service and credentials in .env"
    exit 1
fi

# Step 3: Check psycopg2
print_step "Step 3: Checking Dependencies"
if python -c "import psycopg2" 2>/dev/null; then
    print_success "psycopg2 is installed"
else
    print_warning "Installing psycopg2-binary..."
    pip install psycopg2-binary
    print_success "psycopg2-binary installed"
fi

# Step 4: Export SQLite Data
print_step "Step 4: Exporting Data from SQLite"
echo "Exporting data (this may take a minute)..."

# Make sure we're using SQLite
export USE_SQLITE=True

python manage.py dumpdata \
    --database=default \
    --natural-foreign \
    --natural-primary \
    --exclude=contenttypes \
    --exclude=auth.permission \
    --exclude=sessions.session \
    --indent=2 \
    > sqlite_data_export_${TIMESTAMP}.json

if [ -f "sqlite_data_export_${TIMESTAMP}.json" ]; then
    EXPORT_SIZE=$(du -h "sqlite_data_export_${TIMESTAMP}.json" | cut -f1)
    print_success "Data exported: sqlite_data_export_${TIMESTAMP}.json ($EXPORT_SIZE)"
else
    print_error "Data export failed!"
    exit 1
fi

# Step 5: Drop and Recreate PostgreSQL Database
print_step "Step 5: Recreating PostgreSQL Database"
print_warning "Dropping existing database if it exists..."

# Use sudo to run as postgres user
sudo -u postgres psql << EOF
-- Drop existing database
DROP DATABASE IF EXISTS $PGDATABASE;

-- Create fresh database
CREATE DATABASE $PGDATABASE
    WITH OWNER = $PGUSER
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TEMPLATE = template0;

-- Grant all privileges
GRANT ALL PRIVILEGES ON DATABASE $PGDATABASE TO $PGUSER;

-- Grant schema privileges
\c $PGDATABASE
GRANT ALL ON SCHEMA public TO $PGUSER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $PGUSER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO $PGUSER;
EOF

print_success "PostgreSQL database recreated"

# Step 6: Apply All Migrations
print_step "Step 6: Applying Migrations to PostgreSQL"

# Switch to PostgreSQL
export USE_SQLITE=False

echo "Running migrations..."
python manage.py migrate

# Verify migrations
MIGRATION_COUNT=$(python manage.py showmigrations news --plan | grep -c '\[X\]' || echo "0")
print_success "Applied $MIGRATION_COUNT migrations to PostgreSQL"

# Step 7: Verify Tables
print_step "Step 7: Verifying Database Schema"

echo "Checking for required tables..."
TABLES=$(psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -t -c "\dt" | wc -l)
print_success "Created $TABLES tables in PostgreSQL"

# Check specific new tables
echo ""
echo "Verifying critical tables:"
for table in news_news news_teammember news_jobopening news_jobapplication news_advertisement; do
    if psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -t -c "\d $table" > /dev/null 2>&1; then
        print_success "  ✓ $table"
    else
        print_error "  ✗ $table MISSING!"
    fi
done

# Step 8: Import Data
print_step "Step 8: Importing Data to PostgreSQL"

echo "Loading data (this may take a few minutes)..."
python manage.py loaddata "sqlite_data_export_${TIMESTAMP}.json" --verbosity=1

print_success "Data imported successfully"

# Step 9: Verify Data
print_step "Step 9: Verifying Data Transfer"

echo "Checking record counts..."
psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" << 'EOF'
SELECT 
    'News Articles' as "Table", COUNT(*) as "Records" FROM news_news
UNION ALL
SELECT 'Team Members', COUNT(*) FROM news_teammember
UNION ALL
SELECT 'Comments', COUNT(*) FROM news_comment
UNION ALL
SELECT 'Subscribers', COUNT(*) FROM news_subscriber
UNION ALL
SELECT 'Share Counts', COUNT(*) FROM news_sharecount
UNION ALL
SELECT 'Job Openings', COUNT(*) FROM news_jobopening
UNION ALL
SELECT 'Job Applications', COUNT(*) FROM news_jobapplication
UNION ALL
SELECT 'Advertisements', COUNT(*) FROM news_advertisement
ORDER BY "Table";
EOF

# Step 10: Update Environment
print_step "Step 10: Updating Configuration"

# Update .env to use PostgreSQL by default
if grep -q "USE_SQLITE" .env 2>/dev/null; then
    sed -i 's/USE_SQLITE=.*/USE_SQLITE=False/' .env
    print_success "Updated .env: USE_SQLITE=False"
else
    echo "USE_SQLITE=False" >> .env
    print_success "Added to .env: USE_SQLITE=False"
fi

# Step 11: Summary
print_step "Migration Complete! ✨"

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                   MIGRATION SUMMARY                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
print_success "✓ SQLite data backed up to: $SQLITE_BACKUP"
print_success "✓ PostgreSQL database recreated"
print_success "✓ All migrations applied (including Jobs & Advertisements)"
print_success "✓ Data successfully transferred"
print_success "✓ Configuration updated to use PostgreSQL"
echo ""
echo "Exported data saved to: sqlite_data_export_${TIMESTAMP}.json"
echo ""
echo "Next Steps:"
echo "  1. Create a superuser for admin access:"
echo "     ${BLUE}python manage.py createsuperuser${NC}"
echo ""
echo "  2. Start the Django server:"
echo "     ${BLUE}python manage.py runserver${NC}"
echo ""
echo "  3. Test the application:"
echo "     Frontend: ${BLUE}http://localhost:3000${NC}"
echo "     Admin:    ${BLUE}http://localhost:3000/admin${NC}"
echo "     API:      ${BLUE}http://localhost:8000/api/${NC}"
echo ""
print_warning "Note: You'll need to create a new superuser since the database was recreated."
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║     Migration completed successfully! 🎉                   ║"
echo "╚════════════════════════════════════════════════════════════╝"
