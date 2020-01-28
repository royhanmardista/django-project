from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from profiles import views as profiles_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', profiles_views.login),
    path('register', profiles_views.register),
    path('profiles', profiles_views.createProfile),
    path('countries', profiles_views.getCountries),
    path('profiles/<int:pk>', profiles_views.profileRUD),
    path('profiles/<int:pk>', profiles_views.profileRUD),
    path('profiles/<int:pk>', profiles_views.profileRUD),
    path('profiles/all', profiles_views.getAllProfiles),   
]

if settings.DEBUG : 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)