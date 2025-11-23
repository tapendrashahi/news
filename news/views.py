from django.shortcuts import render, get_object_or_404
from .models import News, TeamMember

def home(request):
    latest_news = News.objects.order_by('-created_at')[:5]
    return render(request, 'news/home.html', {'latest_news': latest_news})

def category_page(request, category):
    news_list = News.objects.filter(category=category).order_by('-created_at')
    return render(request, 'news/category.html', {
        'category': category.title(),
        'news_list': news_list
    })

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    return render(request, 'news/news_detail.html', {'news': news})

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
