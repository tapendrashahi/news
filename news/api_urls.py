from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import (
    NewsViewSet,
    TeamMemberViewSet,
    CommentViewSet,
    SubscriberViewSet,
    CategoryViewSet,
    JobOpeningViewSet,
    JobApplicationViewSet
)

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'news', NewsViewSet, basename='news')
router.register(r'team', TeamMemberViewSet, basename='team')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'subscribers', SubscriberViewSet, basename='subscriber')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'jobs', JobOpeningViewSet, basename='job')
router.register(r'applications', JobApplicationViewSet, basename='application')

# The API URLs are determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]
