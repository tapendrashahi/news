#!/usr/bin/env python
"""
Script to populate legal pages from JSON files in the administration folder.
Run this script after creating the LegalPage model.
"""

import os
import sys
import django
import json
from datetime import date

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gis.settings')
django.setup()

from news.models import LegalPage


def load_json_file(filename):
    """Load JSON file from administration directory"""
    filepath = os.path.join('administration', filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {filepath} not found")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding {filepath}: {e}")
        return None


def create_or_update_legal_page(page_type, filename, title, slug):
    """Create or update a legal page from JSON file"""
    content = load_json_file(filename)
    if not content:
        return None
    
    # Extract metadata
    metadata = content.get('metadata', {})
    effective_date_str = metadata.get('effectiveDate', '2024-01-01')
    version = metadata.get('version', '1.0')
    contact_email = metadata.get('companyEmail', '')
    
    # Parse effective date
    try:
        effective_date = date.fromisoformat(effective_date_str)
    except (ValueError, TypeError):
        effective_date = date(2024, 1, 1)
    
    # Create or update the page
    page, created = LegalPage.objects.update_or_create(
        page_type=page_type,
        defaults={
            'title': title,
            'slug': slug,
            'content_json': content,
            'status': 'published',
            'version': version,
            'effective_date': effective_date,
            'contact_email': contact_email,
            'meta_description': f'Read our {title} to understand how we handle your data and rights.',
        }
    )
    
    action = "Created" if created else "Updated"
    print(f"✓ {action} {page.get_page_type_display()} (v{page.version})")
    return page


def main():
    """Main function to populate all legal pages"""
    print("Starting legal pages population...")
    print("-" * 50)
    
    pages_config = [
        {
            'page_type': 'privacy_policy',
            'filename': 'privacy_polity.json',
            'title': 'Privacy Policy',
            'slug': 'privacy-policy',
        },
        {
            'page_type': 'terms_of_service',
            'filename': 'terms_of_service.json',
            'title': 'Terms of Service',
            'slug': 'terms-of-service',
        },
        {
            'page_type': 'cookie_policy',
            'filename': 'cookee.json',
            'title': 'Cookie Policy',
            'slug': 'cookie-policy',
        },
        {
            'page_type': 'ethics_policy',
            'filename': 'ethics_policy.json',
            'title': 'Ethics Policy',
            'slug': 'ethics-policy',
        },
        {
            'page_type': 'editorial_guidelines',
            'filename': 'guidemines.json',
            'title': 'Editorial Guidelines',
            'slug': 'editorial-guidelines',
        },
        {
            'page_type': 'about',
            'filename': 'about.json',
            'title': 'About Us',
            'slug': 'about',
        },
    ]
    
    created_count = 0
    updated_count = 0
    
    for config in pages_config:
        try:
            # Check if page exists
            exists = LegalPage.objects.filter(page_type=config['page_type']).exists()
            
            page = create_or_update_legal_page(
                config['page_type'],
                config['filename'],
                config['title'],
                config['slug']
            )
            
            if page:
                if exists:
                    updated_count += 1
                else:
                    created_count += 1
        except Exception as e:
            print(f"✗ Error processing {config['title']}: {e}")
    
    print("-" * 50)
    print(f"Summary: {created_count} created, {updated_count} updated")
    print(f"Total legal pages in database: {LegalPage.objects.count()}")


if __name__ == '__main__':
    main()
