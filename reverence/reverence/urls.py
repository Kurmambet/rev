from django.contrib import admin
from django.urls import include, path
from main import urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
]

