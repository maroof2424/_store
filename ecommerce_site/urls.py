from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products.views import run_migrations 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('run-migrations/', run_migrations, name='run_migrations'),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)