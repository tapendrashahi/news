from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<str:category>/', views.category_page, name='category'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('news/<int:pk>/share/', views.track_share, name='track_share'),
    path('about/', views.about, name='about'),
    path('search/', views.search, name='search'),
    path('privacy/', views.privacy_policy, name='privacy_policy'),
    path('terms/', views.terms_of_service, name='terms_of_service'),
    path('cookies/', views.cookie_policy, name='cookie_policy'),
    path('guidelines/', views.editorial_guidelines, name='editorial_guidelines'),
    path('ethics/', views.ethics_policy, name='ethics_policy'),
]
