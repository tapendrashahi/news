#!/usr/bin/env python
"""Fix advertisement start date to current time"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gis.settings')
django.setup()

from news.models import Advertisement
from django.utils import timezone

# Get the advertisement
ad = Advertisement.objects.get(id=1)
print(f"Advertisement: {ad.title}")
print(f"Current start_date: {ad.start_date}")
print(f"Current server time: {timezone.now()}")

# Set start_date to now
ad.start_date = timezone.now()
ad.save()

print(f"\n✓ Updated start_date to: {ad.start_date}")
print("Advertisement should now be visible!")
