#!/usr/bin/env python
"""Test script to verify Advertisement API"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gis.settings')
django.setup()

from news.models import Advertisement
from django.utils import timezone

print("=" * 50)
print("Advertisement API Test")
print("=" * 50)

# Get all advertisements
all_ads = Advertisement.objects.all()
print(f"\nTotal advertisements in database: {all_ads.count()}")

for ad in all_ads:
    print(f"\n  ID: {ad.id}")
    print(f"  Title: {ad.title}")
    print(f"  Position: {ad.position}")
    print(f"  Is Active: {ad.is_active}")
    print(f"  Start Date: {ad.start_date}")
    print(f"  End Date: {ad.end_date}")
    print(f"  Image: {ad.image}")

# Get active advertisements
now = timezone.now()
active_ads = Advertisement.objects.filter(
    is_active=True,
    start_date__lte=now
)
print(f"\n\nActive advertisements (start_date <= now): {active_ads.count()}")

# Filter sidebar ads
sidebar_ads = active_ads.filter(position='sidebar')
print(f"Active sidebar advertisements: {sidebar_ads.count()}")

for ad in sidebar_ads:
    print(f"\n  ✓ {ad.title}")
    print(f"    Position: {ad.position}")
    print(f"    Image URL: {ad.image.url if ad.image else 'No image'}")
    print(f"    Link: {ad.link_url or 'No link'}")

print("\n" + "=" * 50)
