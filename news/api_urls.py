from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import (
    NewsViewSet,
    TeamMemberViewSet,
    CommentViewSet,
    SubscriberViewSet,
    CategoryViewSet,
    JobOpeningViewSet,
    JobApplicationViewSet,
    AdvertisementViewSet
)
from .api_admin import (
    # Auth endpoints
    get_csrf_token,
    admin_login,
    admin_logout,
    admin_user,
    # Dashboard
    dashboard_stats,
    # Analytics
    analytics,
    # SEO Refinement
    seo_refinement_config,
    # Plagiarism Check
    plagiarism_config,
    # ViewSets
    NewsAdminViewSet,
    TeamAdminViewSet,
    CommentsAdminViewSet,
    SubscribersAdminViewSet,
    AdvertisementsAdminViewSet
)
from .legal_views import LegalPageViewSet
from .ai_views import (
    KeywordSourceViewSet,
    AIArticleViewSet,
    AIGenerationConfigViewSet,
    AIWorkflowLogViewSet,
    NewsSourceConfigViewSet,
    ScrapedArticleViewSet
)

# Public API router
router = DefaultRouter()
router.register(r'news', NewsViewSet, basename='news')
router.register(r'team', TeamMemberViewSet, basename='team')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'subscribers', SubscriberViewSet, basename='subscriber')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'jobs', JobOpeningViewSet, basename='job')
router.register(r'applications', JobApplicationViewSet, basename='application')
router.register(r'advertisements', AdvertisementViewSet, basename='advertisement')
router.register(r'legal', LegalPageViewSet, basename='legal')

# Admin API router
admin_router = DefaultRouter()
admin_router.register(r'news', NewsAdminViewSet, basename='admin-news')
admin_router.register(r'team', TeamAdminViewSet, basename='admin-team')
admin_router.register(r'comments', CommentsAdminViewSet, basename='admin-comments')
admin_router.register(r'subscribers', SubscribersAdminViewSet, basename='admin-subscribers')
admin_router.register(r'advertisements', AdvertisementsAdminViewSet, basename='admin-advertisements')
admin_router.register(r'legal', LegalPageViewSet, basename='admin-legal')

# AI Content Generation API routes (admin only)
admin_router.register(r'ai/keywords', KeywordSourceViewSet, basename='admin-ai-keywords')
admin_router.register(r'ai/articles', AIArticleViewSet, basename='admin-ai-articles')
admin_router.register(r'ai/configs', AIGenerationConfigViewSet, basename='admin-ai-configs')
admin_router.register(r'ai/logs', AIWorkflowLogViewSet, basename='admin-ai-logs')
admin_router.register(r'ai/news-sources', NewsSourceConfigViewSet, basename='admin-ai-news-sources')
admin_router.register(r'ai/scraped-articles', ScrapedArticleViewSet, basename='admin-ai-scraped')

# The API URLs are determined automatically by the router
urlpatterns = [
    # Public API
    path('', include(router.urls)),
    
    # Admin API
    path('admin/auth/csrf/', get_csrf_token, name='admin-csrf'),
    path('admin/auth/login/', admin_login, name='admin-login'),
    path('admin/auth/logout/', admin_logout, name='admin-logout'),
    path('admin/auth/user/', admin_user, name='admin-user'),
    path('admin/dashboard/stats/', dashboard_stats, name='admin-dashboard-stats'),
    path('admin/reports/analytics/', analytics, name='admin-analytics'),
    path('admin/seo-refinement-config/', seo_refinement_config, name='admin-seo-refinement-config'),
    path('admin/plagiarism-config/', plagiarism_config, name='admin-plagiarism-config'),
    path('admin/', include(admin_router.urls)),
]
