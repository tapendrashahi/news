from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

def redirect_to_custom_login(request):
    """Redirect Django admin login to custom login"""
    next_url = request.GET.get('next', '/custom-admin/')
    return redirect(f'/custom-admin/login/?next={next_url}')

urlpatterns = [
    # Redirect Django admin login to custom login
    path('admin/login/', redirect_to_custom_login, name='admin_login_redirect'),
    path('admin/', admin.site.urls),
    path('custom-admin/', include('news.admin_urls')),  # Custom admin panel
    path('', include('news.urls')),   # include your app URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
