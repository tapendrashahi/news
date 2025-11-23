from django.shortcuts import render, get_object_or_404
from .models import News

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
    return render(request, 'news/about.html')
