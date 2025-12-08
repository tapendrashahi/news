from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import News, TeamMember, Comment, ShareCount, Subscriber, JobOpening, JobApplication, Advertisement
from .serializers import (
    NewsListSerializer, NewsDetailSerializer, NewsCreateUpdateSerializer,
    TeamMemberSerializer, CommentSerializer, CommentListSerializer,
    ShareCountSerializer, SubscriberSerializer, CategorySerializer,
    JobOpeningSerializer, JobApplicationSerializer, AdvertisementSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination class"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class NewsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for News model
    Provides CRUD operations and custom actions for news articles
    """
    queryset = News.objects.filter(visibility='public').select_related('author').prefetch_related('comments', 'shares')
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'author']
    search_fields = ['title', 'content', 'excerpt', 'tags']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return NewsListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return NewsCreateUpdateSerializer
        return NewsDetailSerializer
    
    def get_queryset(self):
        """
        Optionally filter by category or search query
        """
        queryset = self.queryset
        
        # Filter by category if provided
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        """Override retrieve to accept slug instead of pk"""
        # Try to get by slug first
        slug = kwargs.get('pk')
        try:
            # Use filter().first() to handle duplicate slugs - get most recent
            instance = News.objects.filter(
                visibility='public',
                slug=slug
            ).select_related('author').prefetch_related('comments', 'shares').order_by('-created_at').first()
            
            if not instance:
                raise News.DoesNotExist
                
        except News.DoesNotExist:
            # If not found by slug, try by pk
            try:
                instance = News.objects.filter(visibility='public').select_related('author').prefetch_related('comments', 'shares').get(pk=slug)
            except (News.DoesNotExist, ValueError):
                return Response(
                    {'error': 'News article not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request, category=None):
        """Get news articles by category"""
        category = request.query_params.get('category')
        if not category:
            return Response(
                {'error': 'Category parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(category=category)
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = NewsListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = NewsListSerializer(queryset, many=True, context={'request': request})
        return Response({
            'category': category,
            'count': queryset.count(),
            'results': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search news articles"""
        query = request.query_params.get('q', '')
        if not query:
            return Response(
                {'error': 'Search query parameter "q" is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(tags__icontains=query)
        )
        
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = NewsListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = NewsListSerializer(queryset, many=True, context={'request': request})
        return Response({
            'query': query,
            'count': queryset.count(),
            'results': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        """Add a comment to a news article"""
        news = self.get_object()
        serializer = CommentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(news=news, is_approved=True)  # Auto-approve for now
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Get all approved comments for a news article"""
        news = self.get_object()
        comments = news.comments.filter(is_approved=True).order_by('-created_at')
        serializer = CommentListSerializer(comments, many=True)
        
        return Response({
            'count': comments.count(),
            'results': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        """Increment share count for a news article"""
        news = self.get_object()
        platform = request.data.get('platform', 'email')
        
        # Validate platform
        valid_platforms = [choice[0] for choice in ShareCount.PLATFORM_CHOICES]
        if platform not in valid_platforms:
            return Response(
                {'error': f'Invalid platform. Choose from: {", ".join(valid_platforms)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get or create share count for this platform
        share_count, created = ShareCount.objects.get_or_create(
            news=news,
            platform=platform,
            defaults={'count': 0}
        )
        
        # Increment count
        share_count.count += 1
        share_count.save()
        
        # Get all shares for this news
        all_shares = news.shares.all()
        total_shares = sum(share.count for share in all_shares)
        
        return Response({
            'platform': platform,
            'count': share_count.count,
            'total_shares': total_shares,
            'platform_shares': {share.platform: share.count for share in all_shares}
        })


class TeamMemberViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for TeamMember model
    Provides list and detail views for team members
    """
    queryset = TeamMember.objects.filter(is_active=True).prefetch_related('articles')
    serializer_class = TeamMemberSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order', 'name', 'joined_date']
    ordering = ['order', 'name']
    
    @action(detail=True, methods=['get'])
    def articles(self, request, pk=None):
        """Get all articles written by this team member"""
        team_member = self.get_object()
        articles = News.objects.filter(
            author=team_member,
            visibility='public'
        ).order_by('-created_at')
        
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(articles, request)
        
        if page is not None:
            serializer = NewsListSerializer(page, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)
        
        serializer = NewsListSerializer(articles, many=True, context={'request': request})
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Comment model
    Provides CRUD operations for comments
    """
    queryset = Comment.objects.filter(is_approved=True)
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['news']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return CommentListSerializer
        return CommentSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new comment"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(is_approved=True)  # Auto-approve for now
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class SubscriberViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Subscriber model
    Provides subscription management
    """
    queryset = Subscriber.objects.filter(is_active=True)
    serializer_class = SubscriberSerializer
    http_method_names = ['get', 'post', 'delete']
    
    def create(self, request, *args, **kwargs):
        """Subscribe to newsletter"""
        email = request.data.get('email')
        
        if not email:
            return Response(
                {'error': 'Email is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if already subscribed
        existing = Subscriber.objects.filter(email=email).first()
        
        if existing:
            if existing.is_active:
                return Response(
                    {'error': 'This email is already subscribed'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                # Reactivate subscription
                existing.is_active = True
                existing.subscribed_at = timezone.now()
                existing.unsubscribed_at = None
                existing.save()
                
                serializer = self.get_serializer(existing)
                return Response({
                    'message': 'Subscription reactivated successfully',
                    'data': serializer.data
                })
        
        # Create new subscription
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'message': 'Successfully subscribed to newsletter',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def unsubscribe(self, request):
        """Unsubscribe from newsletter"""
        email = request.data.get('email')
        
        if not email:
            return Response(
                {'error': 'Email is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            subscriber = Subscriber.objects.get(email=email, is_active=True)
            subscriber.is_active = False
            subscriber.unsubscribed_at = timezone.now()
            subscriber.save()
            
            return Response({
                'message': 'Successfully unsubscribed from newsletter'
            })
        except Subscriber.DoesNotExist:
            return Response(
                {'error': 'Email not found in subscribers list'},
                status=status.HTTP_404_NOT_FOUND
            )


class CategoryViewSet(viewsets.ViewSet):
    """
    ViewSet for category information
    Provides category list with article counts
    """
    
    def list(self, request):
        """Get all categories with article counts"""
        categories = []
        
        # Get counts for each category
        category_counts = News.objects.filter(
            visibility='public'
        ).values('category').annotate(
            count=Count('id')
        )
        
        # Create dictionary for quick lookup
        count_dict = {item['category']: item['count'] for item in category_counts}
        
        # Build response with all categories
        for category_code, category_name in News.CATEGORY_CHOICES:
            categories.append({
                'name': category_code,
                'display_name': category_name,
                'count': count_dict.get(category_code, 0),
                'description': f'{category_name} news and updates'
            })
        
        return Response({
            'categories': categories,
            'total': sum(cat['count'] for cat in categories)
        })


class JobOpeningViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Job Openings
    Provides CRUD operations for job listings
    """
    queryset = JobOpening.objects.filter(is_active=True)
    serializer_class = JobOpeningSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department', 'employment_type', 'experience_level', 'location']
    search_fields = ['title', 'description', 'requirements', 'responsibilities']
    ordering_fields = ['posted_date', 'title']
    ordering = ['-posted_date']
    
    def get_queryset(self):
        """Filter active jobs or all if admin"""
        queryset = self.queryset
        
        # Filter by department if specified
        department = self.request.query_params.get('department', None)
        if department:
            queryset = queryset.filter(department=department)
        
        return queryset


class JobApplicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Job Applications
    Provides CRUD operations for job applications with file upload
    """
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    pagination_class = StandardResultsSetPagination
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'job_opening']
    search_fields = ['full_name', 'email', 'phone']
    ordering_fields = ['applied_date']
    ordering = ['-applied_date']
    
    def create(self, request, *args, **kwargs):
        """Handle job application creation with file upload"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'message': 'Application submitted successfully!',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class AdvertisementViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Advertisements - Public read-only access
    Provides active advertisements for display
    """
    serializer_class = AdvertisementSerializer
    
    def get_queryset(self):
        """Get active advertisements within date range"""
        now = timezone.now()
        queryset = Advertisement.objects.filter(
            is_active=True,
            start_date__lte=now
        ).filter(
            Q(end_date__isnull=True) | Q(end_date__gte=now)
        )
        
        # Filter by position if provided
        position = self.request.query_params.get('position', None)
        if position:
            queryset = queryset.filter(position=position)
        
        return queryset.order_by('order', '-created_at')
    
    @action(detail=True, methods=['post'])
    def track_impression(self, request, pk=None):
        """Track advertisement impression"""
        advertisement = self.get_object()
        advertisement.increment_impressions()
        return Response({'status': 'impression tracked'})
    
    @action(detail=True, methods=['post'])
    def track_click(self, request, pk=None):
        """Track advertisement click"""
        advertisement = self.get_object()
        advertisement.increment_clicks()
        return Response({'status': 'click tracked', 'redirect_url': advertisement.link_url})

