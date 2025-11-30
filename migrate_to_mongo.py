#!/usr/bin/env python
"""
Script to migrate data from SQLite to MongoDB
"""
import os
import django
import sqlite3
from pymongo import MongoClient

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gis.settings')
django.setup()

from news.models import News, TeamMember, Comment

def migrate_data():
    # Connect to SQLite
    sqlite_db = 'db.sqlite3'
    
    if not os.path.exists(sqlite_db):
        print("SQLite database not found. Skipping migration.")
        return
    
    conn = sqlite3.connect(sqlite_db)
    cursor = conn.cursor()
    
    print("Starting data migration from SQLite to MongoDB...")
    
    # Migrate TeamMembers
    try:
        cursor.execute("SELECT * FROM news_teammember")
        team_members = cursor.fetchall()
        
        if team_members:
            print(f"\nMigrating {len(team_members)} team members...")
            for row in team_members:
                TeamMember.objects.create(
                    id=row[0],
                    name=row[1],
                    role=row[2],
                    bio=row[3] or '',
                    photo=row[4] or '',
                    email=row[5] or '',
                    twitter_url=row[6] or '',
                    linkedin_url=row[7] or '',
                    is_active=bool(row[8]),
                    order=row[9],
                    joined_date=row[10]
                )
            print(f"✓ Migrated {len(team_members)} team members")
    except Exception as e:
        print(f"Error migrating team members: {e}")
    
    # Migrate News
    try:
        cursor.execute("SELECT * FROM news_news")
        news_items = cursor.fetchall()
        
        if news_items:
            print(f"\nMigrating {len(news_items)} news articles...")
            for row in news_items:
                author_id = row[6] if len(row) > 6 else None
                author = None
                if author_id:
                    try:
                        author = TeamMember.objects.get(id=author_id)
                    except:
                        pass
                
                News.objects.create(
                    id=row[0],
                    title=row[1],
                    content=row[2],
                    category=row[3] or 'business',
                    created_at=row[4],
                    updated_at=row[5],
                    author=author,
                    image=row[7] if len(row) > 7 else ''
                )
            print(f"✓ Migrated {len(news_items)} news articles")
    except Exception as e:
        print(f"Error migrating news: {e}")
    
    # Migrate Comments
    try:
        cursor.execute("SELECT * FROM news_comment")
        comments = cursor.fetchall()
        
        if comments:
            print(f"\nMigrating {len(comments)} comments...")
            for row in comments:
                try:
                    news = News.objects.get(id=row[1])
                    Comment.objects.create(
                        id=row[0],
                        news=news,
                        name=row[2],
                        email=row[3],
                        text=row[4],
                        created_at=row[5],
                        is_approved=bool(row[6])
                    )
                except Exception as e:
                    print(f"Error migrating comment {row[0]}: {e}")
            print(f"✓ Migrated {len(comments)} comments")
    except Exception as e:
        print(f"Error migrating comments: {e}")
    
    conn.close()
    
    print("\n✅ Data migration completed!")
    print(f"Database: aianalitica")
    print(f"Team Members: {TeamMember.objects.count()}")
    print(f"News Articles: {News.objects.count()}")
    print(f"Comments: {Comment.objects.count()}")

if __name__ == '__main__':
    migrate_data()
