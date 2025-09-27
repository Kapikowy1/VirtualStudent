from django.urls import path, include
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    # path('', home_view, name='home_view'),
]
