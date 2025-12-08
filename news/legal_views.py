from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .legal_models import LegalPage
from .legal_serializers import LegalPageSerializer, LegalPageListSerializer
from .permissions import IsAdmin


class LegalPageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing legal/administrative pages
    
    Admin endpoints require authentication
    Public endpoints are available without authentication
    """
    queryset = LegalPage.objects.all()
    serializer_class = LegalPageSerializer
    
    def get_permissions(self):
        """
        Public can read published pages
        Only admins can create/update/delete
        """
        if self.action in ['list', 'retrieve', 'get_by_slug', 'get_by_type']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsAdmin]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """Use lightweight serializer for list view"""
        if self.action == 'list':
            return LegalPageListSerializer
        return LegalPageSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user permissions
        - Admins can see all pages
        - Public can only see published pages
        """
        queryset = LegalPage.objects.all()
        
        # If user is not admin, only show published pages
        if not (self.request.user and self.request.user.is_authenticated and self.request.user.is_staff):
            queryset = queryset.filter(status='published')
        
        # Optional filtering by page_type
        page_type = self.request.query_params.get('page_type', None)
        if page_type:
            queryset = queryset.filter(page_type=page_type)
        
        # Optional filtering by status
        status_param = self.request.query_params.get('status', None)
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        return queryset
    
    @action(detail=False, methods=['get'], url_path='slug/(?P<slug>[^/.]+)')
    def get_by_slug(self, request, slug=None):
        """Get a legal page by its slug"""
        try:
            if request.user and request.user.is_authenticated and request.user.is_staff:
                page = LegalPage.objects.get(slug=slug)
            else:
                page = LegalPage.objects.get(slug=slug, status='published')
            
            serializer = self.get_serializer(page)
            return Response(serializer.data)
        except LegalPage.DoesNotExist:
            return Response(
                {'detail': 'Page not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'], url_path='type/(?P<page_type>[^/.]+)')
    def get_by_type(self, request, page_type=None):
        """Get a legal page by its type"""
        try:
            if request.user and request.user.is_authenticated and request.user.is_staff:
                page = LegalPage.objects.get(page_type=page_type)
            else:
                page = LegalPage.objects.get(page_type=page_type, status='published')
            
            serializer = self.get_serializer(page)
            return Response(serializer.data)
        except LegalPage.DoesNotExist:
            return Response(
                {'detail': 'Page not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Publish a legal page"""
        page = self.get_object()
        page.status = 'published'
        page.save()
        serializer = self.get_serializer(page)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def unpublish(self, request, pk=None):
        """Unpublish a legal page (set to draft)"""
        page = self.get_object()
        page.status = 'draft'
        page.save()
        serializer = self.get_serializer(page)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        """Archive a legal page"""
        page = self.get_object()
        page.status = 'archived'
        page.save()
        serializer = self.get_serializer(page)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def page_types(self, request):
        """Get available page types"""
        return Response({
            'page_types': [
                {'value': choice[0], 'label': choice[1]}
                for choice in LegalPage.PAGE_TYPES
            ]
        })
