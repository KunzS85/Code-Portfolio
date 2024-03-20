from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls import include 
from django.conf.urls.static import static 
from kalender import urls as kalender_urls
from profiles import urls as profiles_urls
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(kalender_urls, namespace="kalender")),
    path("profile/", include(profiles_urls, namespace="profiles")),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
