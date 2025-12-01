from django.urls import path
from . import admin_views

app_name = 'custom_admin'

urlpatterns = [
    # Authentication
    path('login/', admin_views.admin_login, name='login'),
    path('logout/', admin_views.admin_logout, name='logout'),
    
    # Profile
    path('profile/', admin_views.admin_profile, name='profile'),
    
    # Dashboard
    path('', admin_views.admin_dashboard, name='dashboard'),
    
    # News Management
    path('news/', admin_views.admin_news_list, name='news_list'),
    path('news/create/', admin_views.admin_news_create, name='news_create'),
    path('news/<int:pk>/edit/', admin_views.admin_news_edit, name='news_edit'),
    path('news/<int:pk>/delete/', admin_views.admin_news_delete, name='news_delete'),
    
    # Team Management
    path('team/', admin_views.admin_team_list, name='team_list'),
    path('team/create/', admin_views.admin_team_create, name='team_create'),
    path('team/<int:pk>/', admin_views.admin_team_detail, name='team_detail'),
    path('team/<int:pk>/edit/', admin_views.admin_team_edit, name='team_edit'),
    path('team/<int:pk>/delete/', admin_views.admin_team_delete, name='team_delete'),
    
    # Comments Moderation
    path('comments/', admin_views.admin_comments_list, name='comments_list'),
    path('comments/<int:pk>/approve/', admin_views.admin_comment_approve, name='comment_approve'),
    path('comments/<int:pk>/unapprove/', admin_views.admin_comment_unapprove, name='comment_unapprove'),
    path('comments/<int:pk>/delete/', admin_views.admin_comment_delete, name='comment_delete'),
    
    # Subscribers Management
    path('subscribers/', admin_views.admin_subscribers, name='subscribers'),
    path('subscribers/<int:pk>/toggle/', admin_views.admin_subscriber_toggle, name='subscriber_toggle'),
    path('subscribers/<int:pk>/delete/', admin_views.admin_subscriber_delete, name='subscriber_delete'),
    path('subscribers/export/', admin_views.admin_subscribers_export, name='subscribers_export'),
    path('subscribers/bulk-delete/', admin_views.admin_subscribers_bulk_delete, name='subscribers_bulk_delete'),
    
    # Reports
    path('reports/', admin_views.admin_reports, name='reports'),
]
