from django.urls import path
from .views import student_dashboard_view,profile_view

app_name = "students"

urlpatterns = [
    path("", student_dashboard_view, name="dashboard"),
    path("profile/", profile_view, name="profile"),
]
