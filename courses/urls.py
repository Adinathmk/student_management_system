from django.urls import path
from .views import courses_list_view,course_detail_view

app_name = "courses"

urlpatterns = [
    path("", courses_list_view, name="courses"),
    path("<int:course_id>/", course_detail_view, name="detail"),
]
