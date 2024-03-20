from django.urls import path

from . import views

app_name = "material"

urlpatterns = [
    path("", views.MaterialPage.as_view(), name="index"),
] 