from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls import include 
from django.conf.urls.static import static 
from django.contrib.auth import views as auth_views
from alp import urls as alp_urls
from userprofile import urls as profile_urls
from reservation import urls as reservation_urls
from material import urls as material_urls
from application import urls as application_urls
from communication import urls as communication_urls
from django.contrib import admin
from . import views 



admin.site.site_header = 'Die Alp - Administration'
admin.site.index_title = 'Content Administration'
admin.site.site_title = 'Die Alp - Administration'


urlpatterns = [
    path("admin/", admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.LogOutView.as_view(), name='logout'),
    path("", include(alp_urls, namespace="alp")),
    path("profile/", include(profile_urls, namespace="profiles")),
    path("reservation/", include(reservation_urls, namespace="reservation")),
    path("material/", include(material_urls, namespace="material")),
    path("application/", include(application_urls, namespace="application")),
    path("communication/", include(communication_urls, namespace="communication")),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


