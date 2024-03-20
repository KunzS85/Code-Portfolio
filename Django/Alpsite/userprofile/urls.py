from django.urls import path

from . import views

app_name = "profiles"

urlpatterns = [
    path("<int:id>/", views.UserProfilePage.as_view(), name="detail"),
    
] 