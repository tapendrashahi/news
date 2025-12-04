#!/usr/bin/env python
"""
Script to migrate data from SQLite to PostgreSQL
Run this script after setting up PostgreSQL database
"""

import os
import django
import json
from django.core.management import call_command

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gis.settings')
django.setup()

def backup_sqlite_data():
    """Backup SQLite data to JSON"""
    print("📦 Backing up SQLite data...")
    
    # Backup data to JSON file
    with open('sqlite_backup.json', 'w') as f:
        call_command('dumpdata', 
                    '--natural-foreign', 
                    '--natural-primary',
                    '--exclude=contenttypes',
                    '--exclude=auth.permission',
                    '--indent=2',
                    stdout=f)
    
    print("✅ SQLite data backed up to sqlite_backup.json")

def load_postgresql_data():
    """Load data into PostgreSQL"""
    print("📥 Loading data into PostgreSQL...")
    
    # Load data from JSON file
    call_command('loaddata', 'sqlite_backup.json')
    
    print("✅ Data loaded into PostgreSQL successfully")

if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════╗
║       SQLite to PostgreSQL Migration Script             ║
╚══════════════════════════════════════════════════════════╝

IMPORTANT: Before running this script:
1. Install PostgreSQL and create a database named 'news_db'
2. Update gis/settings.py with your PostgreSQL credentials
3. Keep your SQLite database backup safe

This script will:
- Backup SQLite data to JSON
- Run migrations on PostgreSQL
- Import data into PostgreSQL
""")
    
    response = input("Continue with migration? (yes/no): ")
    
    if response.lower() != 'yes':
        print("Migration cancelled.")
        exit(0)
    
    try:
        # Step 1: Backup SQLite data
        backup_sqlite_data()
        
        print("\n📋 Next steps:")
        print("1. Update settings.py to use PostgreSQL")
        print("2. Run: python manage.py migrate")
        print("3. Run this script again to load the data")
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        print("Please check the error and try again.")
