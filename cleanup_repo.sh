#!/bin/bash
# cleanup_repo.sh - Clean up legacy Django template files after React migration

set -e  # Exit on error

echo "🧹 Repository Cleanup Script"
echo "============================"
echo ""
echo "This script will remove legacy Django template files and migration scripts"
echo "that are no longer needed after React migration."
echo ""
read -p "Continue with cleanup? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cleanup cancelled."
    exit 0
fi

echo ""
echo "Starting cleanup..."
echo ""

# Track what we're removing
REMOVED_COUNT=0

# 1. Remove Django templates
if [ -d "news/templates" ]; then
    echo "📁 Removing Django templates..."
    rm -rf news/templates/
    REMOVED_COUNT=$((REMOVED_COUNT + 1))
    echo "   ✓ Removed news/templates/"
fi

# 2. Remove static files
if [ -d "news/static" ]; then
    echo "📁 Removing static CSS files..."
    rm -rf news/static/
    REMOVED_COUNT=$((REMOVED_COUNT + 1))
    echo "   ✓ Removed news/static/"
fi

# 3. Remove migration scripts
echo "📄 Removing old migration scripts..."
FILES_TO_REMOVE=(
    "migrate_to_mongo.py"
    "migrate_to_postgresql.py"
    "migrate_postgres.sh"
    "sync_sqlite_to_mongo.py"
    "sync_to_mongo.py"
    "quick_migration.sh"
    "temp_sqlite_settings.py"
)

for file in "${FILES_TO_REMOVE[@]}"; do
    if [ -f "$file" ]; then
        rm -f "$file"
        REMOVED_COUNT=$((REMOVED_COUNT + 1))
        echo "   ✓ Removed $file"
    fi
done

# 4. Remove test/debug files
echo "📄 Removing test/debug files..."
TEST_FILES=(
    "create_sample_jobs.py"
    "test_admin_api.py"
    "test_ads_api.py"
    "fix_ad_date.py"
    "test_jobs.sql"
)

for file in "${TEST_FILES[@]}"; do
    if [ -f "$file" ]; then
        rm -f "$file"
        REMOVED_COUNT=$((REMOVED_COUNT + 1))
        echo "   ✓ Removed $file"
    fi
done

# 5. Remove backup files
echo "📄 Removing backup files..."
BACKUP_FILES=(
    "db.sqlite3.backup"
    "sqlite_backup.json"
)

for file in "${BACKUP_FILES[@]}"; do
    if [ -f "$file" ]; then
        rm -f "$file"
        REMOVED_COUNT=$((REMOVED_COUNT + 1))
        echo "   ✓ Removed $file"
    fi
done

# 6. Remove old documentation
echo "📄 Removing old documentation files..."
DOC_FILES=(
    "CAREERS_IMPLEMENTATION.md"
    "LEGAL_PAGES_IMPLEMENTATION_PLAN.md"
    "POSTGRESQL_MIGRATION.md"
)

for file in "${DOC_FILES[@]}"; do
    if [ -f "$file" ]; then
        rm -f "$file"
        REMOVED_COUNT=$((REMOVED_COUNT + 1))
        echo "   ✓ Removed $file"
    fi
done

# 7. Remove administration JSON folder
if [ -d "administration" ]; then
    echo "📁 Removing administration JSON files..."
    rm -rf administration/
    REMOVED_COUNT=$((REMOVED_COUNT + 1))
    echo "   ✓ Removed administration/"
fi

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "Summary:"
echo "--------"
echo "Removed items: $REMOVED_COUNT"
echo ""
echo "Cleaned up:"
echo "  ✓ Django templates (replaced by React components)"
echo "  ✓ Static CSS files (replaced by React CSS)"
echo "  ✓ Old migration scripts (migrations completed)"
echo "  ✓ Test/debug files (no longer needed)"
echo "  ✓ Backup files (old backups)"
echo "  ✓ Old documentation (consolidated)"
echo "  ✓ Administration JSON files (loaded into database)"
echo ""
echo "Repository is now cleaner! 🎉"
echo ""
echo "Next steps:"
echo "  1. Review changes: git status"
echo "  2. Test API: python manage.py runserver"
echo "  3. Test React: cd frontend && npm start"
echo "  4. Commit: git add . && git commit -m 'Clean up legacy Django templates'"
