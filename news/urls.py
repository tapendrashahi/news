from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<str:category>/', views.category_page, name='category'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('about/', views.about, name='about'), 
]
