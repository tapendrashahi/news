#!/usr/bin/env python
"""
Test script for Admin API endpoints
Run this script to verify all admin API endpoints are working correctly.
"""

import requests
import json
from pprint import pprint

BASE_URL = "http://localhost:8000/api/admin"
session = requests.Session()

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*80}")
    print(f"TEST: {title}")
    print(f"{'='*80}")
    print(f"Status Code: {response.status_code}")
    print(f"URL: {response.url}")
    try:
        print(f"Response:")
        pprint(response.json())
    except:
        print(response.text)
    print()

def test_auth():
    """Test authentication endpoints"""
    print("\n" + "="*80)
    print("TESTING AUTHENTICATION")
    print("="*80)
    
    # Test login with invalid credentials
    print("\n1. Testing login with invalid credentials...")
    response = session.post(
        f"{BASE_URL}/auth/login/",
        json={"username": "wrong", "password": "wrong"}
    )
    print_response("Login with invalid credentials", response)
    
    # Test login with valid credentials
    print("\n2. Testing login with valid credentials...")
    response = session.post(
        f"{BASE_URL}/auth/login/",
        json={"username": "admin", "password": "admin"}  # Change to your admin credentials
    )
    print_response("Login with valid credentials", response)
    
    if response.status_code == 200:
        # Test get current user
        print("\n3. Testing get current user...")
        response = session.get(f"{BASE_URL}/auth/user/")
        print_response("Get current user", response)
        return True
    else:
        print("⚠️  Login failed! Please update credentials in test script.")
        return False

def test_dashboard():
    """Test dashboard endpoints"""
    print("\n" + "="*80)
    print("TESTING DASHBOARD")
    print("="*80)
    
    response = session.get(f"{BASE_URL}/dashboard/stats/")
    print_response("Get dashboard statistics", response)

def test_news():
    """Test news management endpoints"""
    print("\n" + "="*80)
    print("TESTING NEWS MANAGEMENT")
    print("="*80)
    
    # List news
    print("\n1. List all news...")
    response = session.get(f"{BASE_URL}/news/")
    print_response("List all news", response)
    
    # List with filters
    print("\n2. List news with filters...")
    response = session.get(f"{BASE_URL}/news/?category=tech&page_size=5")
    print_response("List news (filtered by category)", response)
    
    # Get specific news
    if response.status_code == 200 and response.json().get('results'):
        news_id = response.json()['results'][0]['id']
        print(f"\n3. Get news detail (ID: {news_id})...")
        response = session.get(f"{BASE_URL}/news/{news_id}/")
        print_response(f"Get news detail (ID: {news_id})", response)

def test_team():
    """Test team management endpoints"""
    print("\n" + "="*80)
    print("TESTING TEAM MANAGEMENT")
    print("="*80)
    
    # List team members
    response = session.get(f"{BASE_URL}/team/")
    print_response("List all team members", response)
    
    # Get team member articles
    if response.status_code == 200 and response.json().get('results'):
        team_id = response.json()['results'][0]['id']
        print(f"\n2. Get team member articles (ID: {team_id})...")
        response = session.get(f"{BASE_URL}/team/{team_id}/articles/")
        print_response(f"Get team member articles (ID: {team_id})", response)

def test_comments():
    """Test comments moderation endpoints"""
    print("\n" + "="*80)
    print("TESTING COMMENTS MODERATION")
    print("="*80)
    
    # List all comments
    print("\n1. List all comments...")
    response = session.get(f"{BASE_URL}/comments/")
    print_response("List all comments", response)
    
    # List pending comments
    print("\n2. List pending comments...")
    response = session.get(f"{BASE_URL}/comments/?filter=pending")
    print_response("List pending comments", response)
    
    # List approved comments
    print("\n3. List approved comments...")
    response = session.get(f"{BASE_URL}/comments/?filter=approved")
    print_response("List approved comments", response)

def test_subscribers():
    """Test subscribers management endpoints"""
    print("\n" + "="*80)
    print("TESTING SUBSCRIBERS MANAGEMENT")
    print("="*80)
    
    # List subscribers
    print("\n1. List all subscribers...")
    response = session.get(f"{BASE_URL}/subscribers/")
    print_response("List all subscribers", response)
    
    # Get stats
    print("\n2. Get subscriber statistics...")
    response = session.get(f"{BASE_URL}/subscribers/stats/")
    print_response("Get subscriber statistics", response)
    
    # List active subscribers
    print("\n3. List active subscribers...")
    response = session.get(f"{BASE_URL}/subscribers/?status=active&page_size=5")
    print_response("List active subscribers", response)

def test_analytics():
    """Test analytics/reports endpoints"""
    print("\n" + "="*80)
    print("TESTING ANALYTICS & REPORTS")
    print("="*80)
    
    # Get analytics for last 30 days
    print("\n1. Get analytics (last 30 days)...")
    response = session.get(f"{BASE_URL}/reports/analytics/?days=30")
    print_response("Get analytics (30 days)", response)
    
    # Get analytics for last 60 days
    print("\n2. Get analytics (last 60 days)...")
    response = session.get(f"{BASE_URL}/reports/analytics/?days=60")
    print_response("Get analytics (60 days)", response)

def test_logout():
    """Test logout endpoint"""
    print("\n" + "="*80)
    print("TESTING LOGOUT")
    print("="*80)
    
    response = session.post(f"{BASE_URL}/auth/logout/")
    print_response("Logout", response)

def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("ADMIN API ENDPOINT TESTS")
    print("="*80)
    print(f"Base URL: {BASE_URL}")
    print("="*80)
    
    # Test authentication first
    if test_auth():
        # Run all other tests
        test_dashboard()
        test_news()
        test_team()
        test_comments()
        test_subscribers()
        test_analytics()
        test_logout()
        
        print("\n" + "="*80)
        print("ALL TESTS COMPLETED!")
        print("="*80)
    else:
        print("\n⚠️  Tests aborted due to authentication failure.")
        print("Please update admin credentials in the test script.")

if __name__ == "__main__":
    main()
