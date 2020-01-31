from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from profiles import views as profiles_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', profiles_views.login, name="login"),
    path('user', profiles_views.findLoggedUser, name="loggeduser"),
    path('users', profiles_views.getAllUsers, name="allusers"),
    path('register', profiles_views.register,name="register"),
    path('countries', profiles_views.getCountries, name="countries"),
    path('profiles', profiles_views.createProfile, name="createprofile"),
    path('profiles/all', profiles_views.getAllProfiles, name="getprofiles"),   
    path('profiles/<int:pk>', profiles_views.profileRUD, name="read_update_delete"),    
]

if settings.DEBUG : 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)