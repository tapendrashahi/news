from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import News, TeamMember, Comment, ShareCount
from django.contrib.auth.models import User


def admin_login(request):
    """Custom admin login view"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('custom_admin:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_staff:
                login(request, user)
                
                # Set session expiry based on 'remember me'
                if not remember:
                    request.session.set_expiry(0)  # Session expires when browser closes
                
                messages.success(request, f'Welcome back, {user.username}!')
                
                # Redirect to 'next' parameter or dashboard
                next_url = request.GET.get('next', 'custom_admin:dashboard')
                return redirect(next_url)
            else:
                messages.error(request, 'You do not have permission to access the admin area.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'admin/custom_login.html')


def admin_logout(request):
    """Custom admin logout view"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('custom_admin:login')


@staff_member_required
def admin_dashboard(request):
    """Main admin dashboard with statistics"""
    
    # Get statistics
    total_news = News.objects.count()
    total_team = TeamMember.objects.filter(is_active=True).count()
    total_comments = Comment.objects.count()
    pending_comments = Comment.objects.filter(is_approved=False).count()
    
    # Recent activity
    recent_news = News.objects.order_by('-created_at')[:5]
    recent_comments = Comment.objects.order_by('-created_at')[:5]
    
    # Category breakdown
    categories = News.objects.values('category').annotate(count=Count('id'))
    
    # Monthly stats
    thirty_days_ago = timezone.now() - timedelta(days=30)
    news_last_month = News.objects.filter(created_at__gte=thirty_days_ago).count()
    comments_last_month = Comment.objects.filter(created_at__gte=thirty_days_ago).count()
    
    # Top shared articles
    top_shared = []
    for news in News.objects.all()[:10]:
        total_shares = ShareCount.objects.filter(news=news).aggregate(
            total=Count('id')
        )['total'] or 0
        if total_shares > 0:
            top_shared.append({'news': news, 'shares': total_shares})
    top_shared.sort(key=lambda x: x['shares'], reverse=True)
    top_shared = top_shared[:5]
    
    context = {
        'total_news': total_news,
        'total_team': total_team,
        'total_comments': total_comments,
        'pending_comments': pending_comments,
        'recent_news': recent_news,
        'recent_comments': recent_comments,
        'categories': categories,
        'news_last_month': news_last_month,
        'comments_last_month': comments_last_month,
        'top_shared': top_shared,
    }
    
    return render(request, 'admin/custom_admin.html', context)

@staff_member_required
def admin_news_list(request):
    """List all news articles with filters"""
    category = request.GET.get('category', '')
    search = request.GET.get('search', '')
    
    news_list = News.objects.all().order_by('-created_at')
    
    if category:
        news_list = news_list.filter(category=category)
    
    if search:
        news_list = news_list.filter(
            Q(title__icontains=search) | Q(content__icontains=search)
        )
    
    context = {
        'news_list': news_list,
        'category': category,
        'search': search,
        'categories': News.CATEGORY_CHOICES,
    }
    
    return render(request, 'admin/custom_news_list.html', context)

@staff_member_required
def admin_news_create(request):
    """Create new news article"""
    if request.method == 'POST':
        title = request.POST.get('title')
        slug = request.POST.get('slug')
        content = request.POST.get('content')
        excerpt = request.POST.get('excerpt', '')
        category = request.POST.get('category')
        tags = request.POST.get('tags', '')
        author_id = request.POST.get('author')
        meta_description = request.POST.get('meta_description', '')
        visibility = request.POST.get('visibility', 'public')
        publish_date = request.POST.get('publish_date')
        image = request.FILES.get('image')
        
        if title and content and category:
            news = News.objects.create(
                title=title,
                slug=slug if slug else '',
                content=content,
                excerpt=excerpt,
                category=category,
                tags=tags,
                author_id=author_id if author_id else None,
                meta_description=meta_description,
                visibility=visibility,
                publish_date=publish_date if publish_date else None,
                image=image if image else None
            )
            messages.success(request, f'News article "{title}" created successfully!')
            return redirect('custom_admin:news_list')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    team_members = TeamMember.objects.filter(is_active=True)
    
    context = {
        'news': News(),  # Empty news object for form
        'team_members': team_members,
        'categories': News.CATEGORY_CHOICES,
    }
    
    return render(request, 'admin/add_news.html', context)

@staff_member_required
def admin_news_edit(request, pk):
    """Edit existing news article"""
    news = get_object_or_404(News, pk=pk)
    
    if request.method == 'POST':
        news.title = request.POST.get('title')
        news.slug = request.POST.get('slug', '')
        news.content = request.POST.get('content')
        news.excerpt = request.POST.get('excerpt', '')
        news.category = request.POST.get('category')
        news.tags = request.POST.get('tags', '')
        news.meta_description = request.POST.get('meta_description', '')
        news.visibility = request.POST.get('visibility', 'public')
        publish_date = request.POST.get('publish_date')
        news.publish_date = publish_date if publish_date else None
        
        author_id = request.POST.get('author')
        news.author_id = author_id if author_id else None
        
        if request.FILES.get('image'):
            news.image = request.FILES.get('image')
        
        news.save()
        messages.success(request, f'News article "{news.title}" updated successfully!')
        return redirect('custom_admin:news_list')
    
    team_members = TeamMember.objects.filter(is_active=True)
    
    context = {
        'news': news,
        'team_members': team_members,
        'categories': News.CATEGORY_CHOICES,
        'is_edit': True,
    }
    
    return render(request, 'admin/add_news.html', context)

@staff_member_required
def admin_news_delete(request, pk):
    """Delete news article"""
    news = get_object_or_404(News, pk=pk)
    title = news.title
    news.delete()
    messages.success(request, f'News article "{title}" deleted successfully!')
    return redirect('custom_admin:news_list')

@staff_member_required
def admin_team_list(request):
    """List all team members"""
    team_members = TeamMember.objects.all().order_by('order', 'name')
    
    context = {
        'team_members': team_members,
    }
    
    return render(request, 'admin/custom_team_list.html', context)

@staff_member_required
def admin_team_create(request):
    """Create new team member"""
    if request.method == 'POST':
        name = request.POST.get('name')
        role = request.POST.get('role')
        bio = request.POST.get('bio', '')
        email = request.POST.get('email', '')
        twitter_url = request.POST.get('twitter_url', '')
        linkedin_url = request.POST.get('linkedin_url', '')
        order = request.POST.get('order', 0)
        photo = request.FILES.get('photo')
        
        if name and role:
            team_member = TeamMember.objects.create(
                name=name,
                role=role,
                bio=bio,
                email=email,
                twitter_url=twitter_url,
                linkedin_url=linkedin_url,
                order=order,
                photo=photo if photo else None
            )
            messages.success(request, f'Team member "{name}" added successfully!')
            return redirect('custom_admin:team_list')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    context = {
        'team_member': TeamMember(),
        'roles': TeamMember.ROLE_CHOICES,
    }
    
    return render(request, 'admin/custom_team_form.html', context)

@staff_member_required
def admin_team_edit(request, pk):
    """Edit team member"""
    team_member = get_object_or_404(TeamMember, pk=pk)
    
    if request.method == 'POST':
        team_member.name = request.POST.get('name')
        team_member.role = request.POST.get('role')
        team_member.bio = request.POST.get('bio', '')
        team_member.email = request.POST.get('email', '')
        team_member.twitter_url = request.POST.get('twitter_url', '')
        team_member.linkedin_url = request.POST.get('linkedin_url', '')
        team_member.order = request.POST.get('order', 0)
        team_member.is_active = request.POST.get('is_active') == 'on'
        
        if request.FILES.get('photo'):
            team_member.photo = request.FILES.get('photo')
        
        team_member.save()
        messages.success(request, f'Team member "{team_member.name}" updated successfully!')
        return redirect('custom_admin:team_list')
    
    context = {
        'team_member': team_member,
        'roles': TeamMember.ROLE_CHOICES,
        'is_edit': True,
    }
    
    return render(request, 'admin/custom_team_form.html', context)

@staff_member_required
def admin_team_delete(request, pk):
    """Delete team member"""
    team_member = get_object_or_404(TeamMember, pk=pk)
    name = team_member.name
    team_member.delete()
    messages.success(request, f'Team member "{name}" deleted successfully!')
    return redirect('custom_admin:team_list')

@staff_member_required
def admin_comments_list(request):
    """List all comments with moderation"""
    filter_type = request.GET.get('filter', 'all')
    
    if filter_type == 'pending':
        comments = Comment.objects.filter(is_approved=False)
    elif filter_type == 'approved':
        comments = Comment.objects.filter(is_approved=True)
    else:
        comments = Comment.objects.all()
    
    comments = comments.order_by('-created_at')
    
    context = {
        'comments': comments,
        'filter': filter_type,
    }
    
    return render(request, 'admin/custom_comments.html', context)

@staff_member_required
def admin_comment_approve(request, pk):
    """Approve a comment"""
    comment = get_object_or_404(Comment, pk=pk)
    comment.is_approved = True
    comment.save()
    messages.success(request, 'Comment approved successfully!')
    return redirect('custom_admin:comments_list')

@staff_member_required
def admin_comment_unapprove(request, pk):
    """Unapprove a comment"""
    comment = get_object_or_404(Comment, pk=pk)
    comment.is_approved = False
    comment.save()
    messages.success(request, 'Comment unapproved successfully!')
    return redirect('custom_admin:comments_list')

@staff_member_required
def admin_comment_delete(request, pk):
    """Delete a comment"""
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    messages.success(request, 'Comment deleted successfully!')
    return redirect('custom_admin:comments_list')

@staff_member_required
def admin_reports(request):
    """Analytics and reports page"""
    
    # Date range
    days = int(request.GET.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)
    
    # News statistics
    total_news = News.objects.count()
    news_period = News.objects.filter(created_at__gte=start_date).count()
    
    # Category breakdown
    category_stats = []
    for cat_code, cat_name in News.CATEGORY_CHOICES:
        count = News.objects.filter(category=cat_code).count()
        category_stats.append({
            'name': cat_name,
            'count': count,
            'percentage': (count / total_news * 100) if total_news > 0 else 0
        })
    
    # Comments statistics
    total_comments = Comment.objects.count()
    approved_comments = Comment.objects.filter(is_approved=True).count()
    pending_comments = Comment.objects.filter(is_approved=False).count()
    comments_period = Comment.objects.filter(created_at__gte=start_date).count()
    approval_rate = int((approved_comments / total_comments * 100)) if total_comments > 0 else 0
    
    # Share statistics
    share_stats = []
    for platform in ['facebook', 'twitter', 'linkedin', 'email']:
        total = sum([sc.count for sc in ShareCount.objects.filter(platform=platform)])
        share_stats.append({
            'platform': platform.title(),
            'count': total
        })
    
    # Top authors
    top_authors = []
    for member in TeamMember.objects.all():
        article_count = News.objects.filter(author=member).count()
        if article_count > 0:
            top_authors.append({
                'name': member.name,
                'count': article_count
            })
    top_authors.sort(key=lambda x: x['count'], reverse=True)
    top_authors = top_authors[:5]
    
    # Most commented articles
    most_commented = []
    for news in News.objects.all():
        comment_count = Comment.objects.filter(news=news, is_approved=True).count()
        if comment_count > 0:
            most_commented.append({
                'news': news,
                'count': comment_count
            })
    most_commented.sort(key=lambda x: x['count'], reverse=True)
    most_commented = most_commented[:5]
    
    context = {
        'days': days,
        'total_news': total_news,
        'news_period': news_period,
        'category_stats': category_stats,
        'total_comments': total_comments,
        'approved_comments': approved_comments,
        'pending_comments': pending_comments,
        'comments_period': comments_period,
        'approval_rate': approval_rate,
        'share_stats': share_stats,
        'top_authors': top_authors,
        'most_commented': most_commented,
    }
    
    return render(request, 'admin/custom_reports.html', context)
