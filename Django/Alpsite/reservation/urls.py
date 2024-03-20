from django.urls import path

from . import views

app_name = "reservation"

urlpatterns = [
    path("", views.ReservationPage.as_view(), name="reservation"),
    path("maintenance", views.MaintenancePage.as_view(), name="maintenance"),
] 