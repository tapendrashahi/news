from django.urls import path
from . import admin_views

app_name = 'custom_admin'

urlpatterns = [
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
    path('team/<int:pk>/edit/', admin_views.admin_team_edit, name='team_edit'),
    path('team/<int:pk>/delete/', admin_views.admin_team_delete, name='team_delete'),
    
    # Comments Moderation
    path('comments/', admin_views.admin_comments_list, name='comments_list'),
    path('comments/<int:pk>/approve/', admin_views.admin_comment_approve, name='comment_approve'),
    path('comments/<int:pk>/unapprove/', admin_views.admin_comment_unapprove, name='comment_unapprove'),
    path('comments/<int:pk>/delete/', admin_views.admin_comment_delete, name='comment_delete'),
    
    # Reports
    path('reports/', admin_views.admin_reports, name='reports'),
]
