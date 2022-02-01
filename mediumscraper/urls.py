from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('scraper.urls')),
]

handler404 = 'scraper.views.error_404_view'