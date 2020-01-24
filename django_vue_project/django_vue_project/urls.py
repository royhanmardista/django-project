from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from profiles import views as profiles_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', profiles_views.login),
    path('register', profiles_views.register),
    path('profiles/create', profiles_views.createProfile),
    path('profiles/all', profiles_views.getAllProfiles)
]
