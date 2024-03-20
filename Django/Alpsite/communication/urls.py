from django.urls import path

from . import views

app_name = "communication"

urlpatterns = [
    path("pwreset", views.PwResetPage.as_view(), name="pwreset"),
    path("pwreset/<int:id>/", views.PwResetFormPage.as_view(), name="pwresetform")
] 