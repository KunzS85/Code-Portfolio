from django.urls import path

from . import views

app_name = "kalender"

urlpatterns = [
    path("", views.HomePage.as_view(), name="index"),
    path("calendar/<int:pk>/", views.DayCalendarPage.as_view(), name="calendar"),
    path("weekcalendar/<int:pk>/", views.WeekCalendar2Page.as_view(), name="week"),
    path("hourdetail/<int:pk>/", views.OccupancyDetailPage.as_view(), name="hour"),
    
] 