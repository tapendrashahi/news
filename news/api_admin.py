from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, Q
from django.utils import timezone
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from datetime import timedelta
import csv

from .models import News, TeamMember, Comment, ShareCount, Subscriber, Advertisement
from .serializers import (
    NewsAdminSerializer, TeamMemberAdminSerializer, CommentAdminSerializer,
    SubscriberAdminSerializer, DashboardStatsSerializer, AnalyticsSerializer,
    NewsListSerializer, AdvertisementAdminSerializer
)
from .permissions import IsAdmin


# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@api_view(['GET'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def get_csrf_token(request):
    """Get CSRF token for session"""
    return Response({'detail': 'CSRF cookie set'})


@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login(request):
    """Admin login endpoint"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        if user.is_staff:
            login(request, user)
            return Response({
                'success': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser
                }
            })
        else:
            return Response(
                {'error': 'You do not have permission to access the admin area'},
                status=status.HTTP_403_FORBIDDEN
            )
    else:
        return Response(
            {'error': 'Invalid username or password'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_logout(request):
    """Admin logout endpoint"""
    logout(request)
    return Response({'success': True, 'message': 'Logged out successfully'})


@api_view(['GET'])
@permission_classes([IsAdmin])
def admin_user(request):
    """Get current admin user info"""
    user = request.user
    
    # Try to find associated team member
    team_member = None
    try:
        if user.email:
            team_member = TeamMember.objects.filter(email=user.email).first()
        if not team_member:
            full_name = user.get_full_name()
            if full_name:
                team_member = TeamMember.objects.filter(name__icontains=full_name).first()
    except:
        pass
    
    data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
        'team_member': TeamMemberAdminSerializer(team_member).data if team_member else None
    }
    
    return Response(data)


# ============================================================================
# DASHBOARD ENDPOINTS
# ============================================================================

@api_view(['GET'])
@permission_classes([IsAdmin])
def dashboard_stats(request):
    """Get dashboard statistics"""
    
    # Get statistics
    total_news = News.objects.count()
    total_team = TeamMember.objects.filter(is_active=True).count()
    total_comments = Comment.objects.count()
    pending_comments = Comment.objects.filter(is_approved=False).count()
    total_subscribers = Subscriber.objects.count()
    active_subscribers = Subscriber.objects.filter(is_active=True).count()
    
    # Recent activity
    recent_news = News.objects.order_by('-created_at')[:5]
    recent_comments = Comment.objects.order_by('-created_at')[:5]
    
    # Category breakdown
    categories = []
    for cat_code, cat_name in News.CATEGORY_CHOICES:
        count = News.objects.filter(category=cat_code).count()
        categories.append({
            'code': cat_code,
            'name': cat_name,
            'count': count
        })
    
    # Monthly stats
    thirty_days_ago = timezone.now() - timedelta(days=30)
    news_last_month = News.objects.filter(created_at__gte=thirty_days_ago).count()
    comments_last_month = Comment.objects.filter(created_at__gte=thirty_days_ago).count()
    
    # Top shared articles
    top_shared = []
    for news in News.objects.all()[:20]:
        total_shares = sum(share.count for share in news.shares.all())
        if total_shares > 0:
            top_shared.append({
                'news': {
                    'id': news.id,
                    'title': news.title,
                    'slug': news.slug
                },
                'shares': total_shares
            })
    top_shared.sort(key=lambda x: x['shares'], reverse=True)
    top_shared = top_shared[:5]
    
    data = {
        'total_news': total_news,
        'total_team': total_team,
        'total_comments': total_comments,
        'pending_comments': pending_comments,
        'total_subscribers': total_subscribers,
        'active_subscribers': active_subscribers,
        'news_last_month': news_last_month,
        'comments_last_month': comments_last_month,
        'recent_news': NewsListSerializer(recent_news, many=True, context={'request': request}).data,
        'recent_comments': CommentAdminSerializer(recent_comments, many=True).data,
        'categories': categories,
        'top_shared': top_shared
    }
    
    return Response(data)


# ============================================================================
# NEWS ADMIN VIEWSET
# ============================================================================

class NewsAdminViewSet(viewsets.ModelViewSet):
    """Admin viewset for managing news articles"""
    queryset = News.objects.all().select_related('author').prefetch_related('comments', 'shares')
    serializer_class = NewsAdminSerializer
    permission_classes = [IsAdmin]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_queryset(self):
        """Filter news by category, search, visibility"""
        queryset = self.queryset.order_by('-created_at')
        
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by visibility
        visibility = self.request.query_params.get('visibility', None)
        if visibility:
            queryset = queryset.filter(visibility=visibility)
        
        # Search
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(content__icontains=search) |
                Q(excerpt__icontains=search)
            )
        
        return queryset
    
    def perform_create(self, serializer):
        """Create news article"""
        serializer.save()
    
    def perform_update(self, serializer):
        """Update news article"""
        serializer.save()
    
    @action(detail=True, methods=['post'])
    def upload_image(self, request, pk=None):
        """Upload image for news article"""
        news = self.get_object()
        image = request.FILES.get('image')
        
        if not image:
            return Response(
                {'error': 'No image provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        news.image = image
        news.save()
        
        serializer = self.get_serializer(news)
        return Response(serializer.data)


# ============================================================================
# TEAM ADMIN VIEWSET
# ============================================================================

class TeamAdminViewSet(viewsets.ModelViewSet):
    """Admin viewset for managing team members"""
    queryset = TeamMember.objects.all().order_by('order', 'name')
    serializer_class = TeamMemberAdminSerializer
    permission_classes = [IsAdmin]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    @action(detail=True, methods=['get'])
    def articles(self, request, pk=None):
        """Get articles by this team member"""
        team_member = self.get_object()
        articles = News.objects.filter(author=team_member).order_by('-created_at')
        
        # Pagination
        page_size = int(request.query_params.get('page_size', 10))
        page = int(request.query_params.get('page', 1))
        start = (page - 1) * page_size
        end = start + page_size
        
        total = articles.count()
        articles = articles[start:end]
        
        return Response({
            'count': total,
            'results': NewsListSerializer(articles, many=True, context={'request': request}).data
        })


# ============================================================================
# COMMENTS ADMIN VIEWSET
# ============================================================================

class CommentsAdminViewSet(viewsets.ModelViewSet):
    """Admin viewset for managing comments"""
    queryset = Comment.objects.all().select_related('news').order_by('-created_at')
    serializer_class = CommentAdminSerializer
    permission_classes = [IsAdmin]
    
    def get_queryset(self):
        """Filter comments by approval status"""
        queryset = self.queryset
        
        filter_type = self.request.query_params.get('filter', 'all')
        if filter_type == 'pending':
            queryset = queryset.filter(is_approved=False)
        elif filter_type == 'approved':
            queryset = queryset.filter(is_approved=True)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a comment"""
        comment = self.get_object()
        comment.is_approved = True
        comment.save()
        
        serializer = self.get_serializer(comment)
        return Response({
            'success': True,
            'message': 'Comment approved successfully',
            'comment': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def unapprove(self, request, pk=None):
        """Unapprove a comment"""
        comment = self.get_object()
        comment.is_approved = False
        comment.save()
        
        serializer = self.get_serializer(comment)
        return Response({
            'success': True,
            'message': 'Comment unapproved successfully',
            'comment': serializer.data
        })


# ============================================================================
# SUBSCRIBERS ADMIN VIEWSET
# ============================================================================

class SubscribersAdminViewSet(viewsets.ModelViewSet):
    """Admin viewset for managing subscribers"""
    queryset = Subscriber.objects.all().order_by('-subscribed_at')
    serializer_class = SubscriberAdminSerializer
    permission_classes = [IsAdmin]
    
    def get_queryset(self):
        """Filter subscribers by status and search"""
        queryset = self.queryset
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter == 'active':
            queryset = queryset.filter(is_active=True)
        elif status_filter == 'unsubscribed':
            queryset = queryset.filter(is_active=False)
        
        # Search
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(email__icontains=search) | Q(name__icontains=search)
            )
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get subscriber statistics"""
        total_subscribers = Subscriber.objects.count()
        active_subscribers = Subscriber.objects.filter(is_active=True).count()
        unsubscribed_count = Subscriber.objects.filter(is_active=False).count()
        
        # New this month
        first_of_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        new_this_month = Subscriber.objects.filter(subscribed_at__gte=first_of_month).count()
        
        return Response({
            'total_subscribers': total_subscribers,
            'active_subscribers': active_subscribers,
            'unsubscribed_count': unsubscribed_count,
            'new_this_month': new_this_month
        })
    
    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        """Toggle subscriber active status"""
        subscriber = self.get_object()
        subscriber.is_active = not subscriber.is_active
        
        if not subscriber.is_active:
            subscriber.unsubscribed_at = timezone.now()
        else:
            subscriber.unsubscribed_at = None
        
        subscriber.save()
        
        serializer = self.get_serializer(subscriber)
        status_text = "activated" if subscriber.is_active else "deactivated"
        
        return Response({
            'success': True,
            'message': f'Subscriber {subscriber.email} has been {status_text}',
            'subscriber': serializer.data
        })
    
    @action(detail=False, methods=['post'])
    def bulk_delete(self, request):
        """Bulk delete subscribers"""
        ids = request.data.get('ids', [])
        
        if not ids:
            return Response(
                {'error': 'No subscriber IDs provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        deleted_count = Subscriber.objects.filter(id__in=ids).delete()[0]
        
        return Response({
            'success': True,
            'message': f'{deleted_count} subscriber(s) deleted successfully',
            'deleted_count': deleted_count
        })
    
    @action(detail=False, methods=['get'])
    def export(self, request):
        """Export subscribers to CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="subscribers.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Email', 'Name', 'Status', 'Subscribed At', 'Unsubscribed At'])
        
        subscribers = self.get_queryset()
        for subscriber in subscribers:
            writer.writerow([
                subscriber.email,
                subscriber.name,
                'Active' if subscriber.is_active else 'Unsubscribed',
                subscriber.subscribed_at.strftime('%Y-%m-%d %H:%M'),
                subscriber.unsubscribed_at.strftime('%Y-%m-%d %H:%M') if subscriber.unsubscribed_at else '',
            ])
        
        return response


# ============================================================================
# REPORTS/ANALYTICS ENDPOINTS
# ============================================================================

@api_view(['GET'])
@permission_classes([IsAdmin])
def analytics(request):
    """Get analytics and reports data"""
    
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
            'code': cat_code,
            'name': cat_name,
            'count': count,
            'percentage': round((count / total_news * 100), 2) if total_news > 0 else 0
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
                'id': member.id,
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
                'news': {
                    'id': news.id,
                    'title': news.title,
                    'slug': news.slug
                },
                'count': comment_count
            })
    most_commented.sort(key=lambda x: x['count'], reverse=True)
    most_commented = most_commented[:5]
    
    data = {
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
        'most_commented': most_commented
    }
    
    return Response(data)


# ============================================================================
# ADVERTISEMENTS ADMIN VIEWSET
# ============================================================================

class AdvertisementsAdminViewSet(viewsets.ModelViewSet):
    """Admin ViewSet for managing advertisements"""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementAdminSerializer
    permission_classes = [IsAdmin]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    
    def get_queryset(self):
        """Filter advertisements based on query params"""
        queryset = Advertisement.objects.all()
        
        # Filter by position
        position = self.request.query_params.get('position', None)
        if position:
            queryset = queryset.filter(position=position)
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        # Search by title
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(title__icontains=search)
        
        return queryset.order_by('order', '-created_at')
    
    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        """Toggle advertisement active status"""
        advertisement = self.get_object()
        advertisement.is_active = not advertisement.is_active
        advertisement.save()
        serializer = self.get_serializer(advertisement)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get advertisement statistics"""
        total_ads = Advertisement.objects.count()
        active_ads = Advertisement.objects.filter(is_active=True).count()
        total_clicks = Advertisement.objects.aggregate(total=Count('id'))['total'] or 0
        total_impressions = Advertisement.objects.aggregate(total=Count('id'))['total'] or 0
        
        # Calculate stats
        ads_with_stats = Advertisement.objects.exclude(impressions=0)
        total_clicks_count = sum(ad.clicks for ad in ads_with_stats)
        total_impressions_count = sum(ad.impressions for ad in ads_with_stats)
        avg_ctr = (total_clicks_count / total_impressions_count * 100) if total_impressions_count > 0 else 0
        
        # Top performing ads
        top_ads = Advertisement.objects.filter(is_active=True).order_by('-clicks')[:5]
        
        data = {
            'total_ads': total_ads,
            'active_ads': active_ads,
            'total_clicks': total_clicks_count,
            'total_impressions': total_impressions_count,
            'average_ctr': round(avg_ctr, 2),
            'top_ads': AdvertisementAdminSerializer(top_ads, many=True).data
        }
        
        return Response(data)


# ============================================================================
# SEO REFINEMENT CONFIGURATION ENDPOINT
# ============================================================================

@api_view(['GET', 'POST'])
@permission_classes([IsAdmin])
def seo_refinement_config(request):
    """Get or update SEO refinement configuration"""
    import json
    import os
    from django.conf import settings
    
    config_path = os.path.join(settings.BASE_DIR, 'seo_refinement_config.json')
    
    if request.method == 'GET':
        # Load existing config or return default
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
        else:
            # Default configuration
            config = {
                "seo_refinement": {
                    "enabled": True,
                    "targetScore": 80,
                    "maxRetries": 3,
                    "refinementOptions": {
                        "keywordDensity": {
                            "enabled": True,
                            "targetRange": {"min": 0.5, "max": 2.5},
                            "priority": "high"
                        },
                        "internalLinking": {
                            "enabled": True,
                            "minLinks": 2,
                            "maxLinks": 5,
                            "priority": "medium"
                        },
                        "metaDescription": {
                            "enabled": True,
                            "minLength": 120,
                            "maxLength": 160,
                            "includeKeyword": True,
                            "priority": "high"
                        },
                        "readability": {
                            "enabled": True,
                            "targetScore": 60,
                            "maxSentenceLength": 25,
                            "maxParagraphLength": 150,
                            "priority": "medium"
                        },
                        "titleOptimization": {
                            "enabled": True,
                            "minLength": 30,
                            "maxLength": 60,
                            "includeKeyword": True,
                            "priority": "high"
                        },
                        "contentStructure": {
                            "enabled": True,
                            "minWordCount": 600,
                            "maxWordCount": 2500,
                            "headingDistribution": True,
                            "priority": "low"
                        }
                    },
                    "rewriteStages": {
                        "contentGeneration": {
                            "rewrite": True,
                            "includeSuggestions": True
                        },
                        "humanization": {
                            "rewrite": True,
                            "includeSuggestions": True
                        },
                        "seoOptimization": {
                            "rewrite": False,
                            "includeSuggestions": True
                        }
                    }
                }
            }
        return Response(config)
    
    elif request.method == 'POST':
        # Save configuration
        config = request.data
        
        try:
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            return Response({'success': True, 'message': 'SEO refinement configuration saved successfully'})
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ============================================================================
# PLAGIARISM CHECK CONFIGURATION ENDPOINT
# ============================================================================

@api_view(['GET', 'POST'])
@permission_classes([IsAdmin])
def plagiarism_config(request):
    """Get or update plagiarism check configuration"""
    import json
    import os
    from django.conf import settings
    
    config_path = os.path.join(settings.BASE_DIR, 'plagiarism_config.json')
    
    if request.method == 'GET':
        # Load existing config or return default
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
        else:
            # Default configuration
            config = {
                "plagiarism_check": {
                    "enabled": True,
                    "threshold": 5.0,
                    "maxRetries": 3,
                    "checkOptions": {
                        "checkWeb": {
                            "enabled": True,
                            "description": "Check against web sources"
                        },
                        "checkDatabase": {
                            "enabled": True,
                            "description": "Check against Codequiry database"
                        },
                        "autoRewrite": {
                            "enabled": True,
                            "description": "Automatically rewrite plagiarized sections"
                        }
                    },
                    "rewriteStrategy": {
                        "rewriteSections": {
                            "enabled": True,
                            "description": "Rewrite only plagiarized sections"
                        },
                        "rewriteEntireArticle": {
                            "enabled": False,
                            "description": "Rewrite entire article if plagiarism detected"
                        },
                        "maintainSEO": {
                            "enabled": True,
                            "description": "Maintain SEO optimization during rewrite"
                        },
                        "maintainNepalContext": {
                            "enabled": True,
                            "description": "Maintain Nepal-specific context during rewrite"
                        }
                    },
                    "reportOptions": {
                        "saveReports": {
                            "enabled": True,
                            "description": "Save plagiarism reports for review"
                        },
                        "detailedMatches": {
                            "enabled": True,
                            "description": "Include detailed match information"
                        }
                    }
                }
            }
        return Response(config)
    
    elif request.method == 'POST':
        # Save configuration
        config = request.data
        
        try:
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            return Response({'success': True, 'message': 'Plagiarism check configuration saved successfully'})
        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
