#!/usr/bin/env python
"""
Sync data from SQLite to MongoDB using pymongo directly
"""
import sqlite3
from pymongo import MongoClient
from datetime import datetime

# Connect to databases
sqlite_db = sqlite3.connect('db.sqlite3')
sqlite_db.row_factory = sqlite3.Row
cursor = sqlite_db.cursor()

mongo_client = MongoClient('localhost', 27017)
mongo_db = mongo_client['aianalitica']

print("Starting data sync from SQLite to MongoDB...\n")

# Clear existing MongoDB data
print("Clearing existing MongoDB collections...")
mongo_db.news_teammember.delete_many({})
mongo_db.news_news.delete_many({})
mongo_db.news_comment.delete_many({})
mongo_db.news_sharecount.delete_many({})
print("✓ Cleared\n")

# Sync TeamMembers
print("Syncing Team Members...")
cursor.execute("SELECT * FROM news_teammember")
team_count = 0
for row in cursor.fetchall():
    doc = {
        'id': row['id'],
        'name': row['name'],
        'role': row['role'],
        'bio': row['bio'] or '',
        'photo': row['photo'] or '',
        'email': row['email'] or '',
        'twitter_url': row['twitter_url'] or '',
        'linkedin_url': row['linkedin_url'] or '',
        'is_active': bool(row['is_active']),
        'order': row['order'] or 0,
        'joined_date': row['joined_date']
    }
    mongo_db.news_teammember.insert_one(doc)
    team_count += 1
    print(f"  ✓ {doc['name']} ({doc['role']})")

print(f"Synced {team_count} team members\n")

# Sync News
print("Syncing News Articles...")
cursor.execute("SELECT * FROM news_news")
news_count = 0
for row in cursor.fetchall():
    doc = {
        'id': row['id'],
        'title': row['title'],
        'content': row['content'],
        'category': row['category'],
        'author_id': row['author_id'],
        'created_at': row['created_at'],
        'updated_at': row['updated_at'],
        'image': row['image'] or ''
    }
    mongo_db.news_news.insert_one(doc)
    news_count += 1
    print(f"  ✓ {doc['title'][:50]}...")

print(f"Synced {news_count} news articles\n")

# Sync Comments
print("Syncing Comments...")
cursor.execute("SELECT * FROM news_comment")
comment_count = 0
for row in cursor.fetchall():
    doc = {
        'id': row['id'],
        'news_id': row['news_id'],
        'name': row['name'],
        'email': row['email'],
        'text': row['text'],
        'created_at': row['created_at'],
        'is_approved': bool(row['is_approved'])
    }
    mongo_db.news_comment.insert_one(doc)
    comment_count += 1

print(f"Synced {comment_count} comments\n")

# Sync Share Counts
print("Syncing Share Counts...")
cursor.execute("SELECT * FROM news_sharecount")
share_count = 0
for row in cursor.fetchall():
    doc = {
        'id': row['id'],
        'news_id': row['news_id'],
        'platform': row['platform'],
        'count': row['count'],
        'last_shared': row['last_shared']
    }
    mongo_db.news_sharecount.insert_one(doc)
    share_count += 1

print(f"Synced {share_count} share counts\n")

sqlite_db.close()
mongo_client.close()

print("=" * 50)
print("✓ Data sync completed successfully!")
print("=" * 50)
print(f"\nSummary:")
print(f"  Team Members: {team_count}")
print(f"  News Articles: {news_count}")
print(f"  Comments: {comment_count}")
print(f"  Share Counts: {share_count}")

print("\nVerifying in MongoDB...")
print(f"  news_teammember: {mongo_db.news_teammember.count_documents({})}")
print(f"  news_news: {mongo_db.news_news.count_documents({})}")
print(f"  news_comment: {mongo_db.news_comment.count_documents({})}")
print(f"  news_sharecount: {mongo_db.news_sharecount.count_documents({})}")
