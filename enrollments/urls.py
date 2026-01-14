from django.urls import path
from .views import enroll_course_view

app_name = "enrollments"

urlpatterns = [
    path("enroll/<int:course_id>/", enroll_course_view, name="enroll"),
]
