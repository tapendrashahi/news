#!/usr/bin/env python
"""
Sync data from SQLite to MongoDB
"""
import os
import sys
import django
import sqlite3

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gis.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from news.models import News, TeamMember, Comment, ShareCount

# Connect to SQLite
sqlite_db = sqlite3.connect('db.sqlite3')
sqlite_db.row_factory = sqlite3.Row
cursor = sqlite_db.cursor()

print("Starting data sync from SQLite to MongoDB...\n")

# Clear existing MongoDB data
print("Clearing existing MongoDB data...")
News.objects.all().delete()
TeamMember.objects.all().delete()
Comment.objects.all().delete()
ShareCount.objects.all().delete()
print("✓ Cleared\n")

# Sync TeamMembers
print("Syncing Team Members...")
cursor.execute("SELECT * FROM news_teammember")
team_members = {}
for row in cursor.fetchall():
    tm = TeamMember.objects.create(
        id=row['id'],
        name=row['name'],
        role=row['role'],
        bio=row['bio'] or '',
        email=row['email'] or '',
        twitter_url=row['twitter_url'] or '',
        linkedin_url=row['linkedin_url'] or '',
        is_active=bool(row['is_active']),
        order=row['order'] or 0
    )
    team_members[row['id']] = tm
    print(f"  ✓ {tm.name} ({tm.role})")
print(f"Synced {len(team_members)} team members\n")

# Sync News
print("Syncing News Articles...")
cursor.execute("SELECT * FROM news_news")
news_articles = {}
for row in cursor.fetchall():
    author_id = row['author_id']
    news = News.objects.create(
        id=row['id'],
        title=row['title'],
        content=row['content'],
        category=row['category'],
        author=team_members.get(author_id) if author_id else None,
        created_at=row['created_at'],
        updated_at=row['updated_at']
    )
    news_articles[row['id']] = news
    print(f"  ✓ {news.title[:50]}...")
print(f"Synced {len(news_articles)} news articles\n")

# Sync Comments
print("Syncing Comments...")
cursor.execute("SELECT * FROM news_comment")
comment_count = 0
for row in cursor.fetchall():
    news_id = row['news_id']
    if news_id in news_articles:
        Comment.objects.create(
            id=row['id'],
            news=news_articles[news_id],
            name=row['name'],
            email=row['email'],
            text=row['text'],
            created_at=row['created_at'],
            is_approved=bool(row['is_approved'])
        )
        comment_count += 1
print(f"Synced {comment_count} comments\n")

# Sync Share Counts
print("Syncing Share Counts...")
cursor.execute("SELECT * FROM news_sharecount")
share_count = 0
for row in cursor.fetchall():
    news_id = row['news_id']
    if news_id in news_articles:
        ShareCount.objects.create(
            id=row['id'],
            news=news_articles[news_id],
            platform=row['platform'],
            count=row['count'],
            last_shared=row['last_shared']
        )
        share_count += 1
print(f"Synced {share_count} share counts\n")

sqlite_db.close()

print("=" * 50)
print("✓ Data sync completed successfully!")
print("=" * 50)
print(f"\nSummary:")
print(f"  Team Members: {len(team_members)}")
print(f"  News Articles: {len(news_articles)}")
print(f"  Comments: {comment_count}")
print(f"  Share Counts: {share_count}")
