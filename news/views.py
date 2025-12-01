from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import News, TeamMember, Comment, ShareCount
import json
import os

def home(request):
    # Get latest news articles for display
    latest_news = News.objects.order_by('-created_at')[:15]
    
    # Get category counts
    category_counts = News.objects.values('category').annotate(count=Count('category'))
    category_dict = {item['category']: item['count'] for item in category_counts}
    
    context = {
        'latest_news': latest_news,
        'business_count': category_dict.get('business', 0),
        'political_count': category_dict.get('political', 0),
        'tech_count': category_dict.get('tech', 0),
        'education_count': category_dict.get('education', 0),
    }
    
    return render(request, 'news/home.html', context)

def search(request):
    query = request.GET.get('q', '')
    results = []
    
    if query:
        # Search in title, content, and category
        results = News.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) | 
            Q(category__icontains=query)
        ).order_by('-created_at')
    
    context = {
        'query': query,
        'results': results,
        'count': results.count() if results else 0
    }
    
    return render(request, 'news/search_results.html', context)

def category_page(request, category):
    news_list = News.objects.filter(category=category).order_by('-created_at')
    
    # Pagination - 10 articles per page
    paginator = Paginator(news_list, 10)
    page = request.GET.get('page', 1)
    
    try:
        news_page = paginator.page(page)
    except PageNotAnInteger:
        news_page = paginator.page(1)
    except EmptyPage:
        news_page = paginator.page(paginator.num_pages)
    
    return render(request, 'news/category.html', {
        'category': category.title(),
        'news_list': news_page,
        'paginator': paginator,
    })

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    
    # Handle comment submission
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        text = request.POST.get('text', '').strip()
        
        if name and email and text:
            Comment.objects.create(
                news=news,
                name=name,
                email=email,
                text=text
            )
            messages.success(request, 'Your comment has been posted successfully!')
            return redirect('news:news_detail', pk=pk)
        else:
            messages.error(request, 'Please fill in all fields.')
    
    # Get approved comments for this article
    comments = news.comments.filter(is_approved=True).order_by('-created_at')
    comment_count = comments.count()
    
    # Get related articles from the same category
    related_articles = News.objects.filter(category=news.category).exclude(pk=pk).order_by('-created_at')[:3]
    
    # Get share counts for this article
    share_counts = {}
    for platform in ['facebook', 'twitter', 'linkedin', 'email']:
        try:
            share = ShareCount.objects.get(news=news, platform=platform)
            share_counts[platform] = share.count
        except ShareCount.DoesNotExist:
            share_counts[platform] = 0
    
    total_shares = sum(share_counts.values())
    
    context = {
        'news': news,
        'comments': comments,
        'comment_count': comment_count,
        'related_articles': related_articles,
        'share_counts': share_counts,
        'total_shares': total_shares,
    }
    
    return render(request, 'news/news_detail.html', context)


@require_POST
def track_share(request, pk):
    """Track social media shares"""
    try:
        news = get_object_or_404(News, pk=pk)
        platform = request.POST.get('platform')
        
        if platform not in ['facebook', 'twitter', 'linkedin', 'email']:
            return JsonResponse({'success': False, 'error': 'Invalid platform'}, status=400)
        
        # Get or create share count record
        share, created = ShareCount.objects.get_or_create(
            news=news,
            platform=platform,
            defaults={'count': 0}
        )
        
        # Increment the count
        share.count += 1
        share.save()
        
        return JsonResponse({
            'success': True,
            'count': share.count,
            'platform': platform
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def about(request):
    # Get real statistics from database
    total_articles = News.objects.count()
    
    # Format numbers for display
    def format_number(num):
        if num >= 1000000:
            return f"{num / 1000000:.1f}M+"
        elif num >= 1000:
            return f"{num / 1000:.1f}K+"
        else:
            return f"{num}+"
    
    # Calculate monthly readers (example: based on article views or a static multiplier)
    # For now, using a formula: articles * average views per article
    monthly_readers_raw = total_articles * 500 if total_articles > 0 else 0
    
    # Get active team members
    team_members = TeamMember.objects.filter(is_active=True).order_by('order', 'name')
    expert_journalists = team_members.count()
    
    context = {
        'total_articles': total_articles,
        'total_articles_formatted': format_number(total_articles),
        'monthly_readers': monthly_readers_raw,
        'monthly_readers_formatted': format_number(monthly_readers_raw),
        'expert_journalists': expert_journalists if expert_journalists > 0 else 4,
        'team_members': team_members,
    }
    
    return render(request, 'news/about.html', context)

def privacy_policy(request):
    """Privacy Policy page with JSON data"""
    # Load privacy policy data from JSON file
    json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'administration', 'privacy_polity.json')
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            privacy_data = json.load(f)
    except FileNotFoundError:
        # Fallback data if JSON file is not found
        privacy_data = {
            'metadata': {
                'title': 'Privacy Policy',
                'lastUpdated': '2024-12-01',
                'companyName': 'News Portal'
            },
            'introduction': {
                'title': 'Introduction',
                'content': ['Welcome to our privacy policy.']
            },
            'sections': []
        }
    
    # Convert to JSON string for JavaScript
    privacy_data_json = json.dumps(privacy_data)
    
    context = {
        'privacy_data': privacy_data_json
    }
    
    return render(request, 'news/privacy_policy.html', context)

def terms_of_service(request):
    """Terms of Service page with JSON data"""
    # Load terms of service data from JSON file
    json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'administration', 'terms_of_service.json')
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            terms_data = json.load(f)
    except FileNotFoundError:
        # Fallback data if JSON file is not found
        terms_data = {
            'metadata': {
                'title': 'Terms of Service',
                'lastUpdated': '2024-12-01',
                'companyName': 'News Portal'
            },
            'introduction': {
                'title': 'Introduction',
                'content': ['Welcome to our terms of service.']
            },
            'sections': []
        }
    
    # Convert to JSON string for JavaScript
    terms_data_json = json.dumps(terms_data)
    
    context = {
        'terms_data': terms_data_json
    }
    
    return render(request, 'news/terms_of_service.html', context)

def cookie_policy(request):
    """Cookie Policy page with JSON data"""
    # Load cookie policy data from JSON file
    json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'administration', 'cookee.json')
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            cookie_data = json.load(f)
    except FileNotFoundError:
        # Fallback data if JSON file is not found
        cookie_data = {
            'metadata': {
                'title': 'Cookie Policy',
                'lastUpdated': '2024-12-01',
                'companyName': 'News Portal'
            },
            'introduction': {
                'title': 'Introduction',
                'content': ['Welcome to our cookie policy.']
            },
            'sections': []
        }
    
    # Convert to JSON string for JavaScript
    cookie_data_json = json.dumps(cookie_data)
    
    context = {
        'cookie_data': cookie_data_json
    }
    
    return render(request, 'news/cookee.html', context)
