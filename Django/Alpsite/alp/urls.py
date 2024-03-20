from django.urls import path

from . import views

app_name = "alp"

urlpatterns = [
    path("", views.HomePage.as_view(), name="home"),
    path("information/", views.InformationPage.as_view(), name="information"),
    path("information/<int:pk>", views.InformationDetailPage.as_view(), name="info_detail"),
    path("gallery/", views.GalleryPage.as_view(), name="gallery"),
    path("contact/", views.ContactPage.as_view(), name="contact"),
    
] 