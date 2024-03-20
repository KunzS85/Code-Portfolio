from django.urls import path

from . import views

app_name = "application"

urlpatterns = [
    path("applicationForm", views.ApplicationFormView.as_view(), name="applicationForm"),
    path("<int:id>/", views.ApplicationAcceptanceView.as_view(), name="userinfo"),
    path("decision/<int:id>/", views.UserDecisionView.as_view(), name="decision"),
] 