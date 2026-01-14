from django.urls import path
from . import views

app_name = "admin_panel"

urlpatterns = [
    path("", views.admin_dashboard, name="dashboard"),

    path("students/", views.students_management, name="students"),
    path("students/add/", views.add_student, name="add_student"),
    path("students/<int:pk>/edit/", views.edit_student, name="edit_student"),
    path("students/<int:pk>/delete/", views.delete_student, name="delete_student"),

    path("courses/", views.courses_management, name="courses"),
    path("courses/add/", views.add_course, name="add_course"),
    path("courses/<int:pk>/edit/", views.edit_course, name="edit_course"),
    path("courses/<int:pk>/delete/", views.delete_course, name="delete_course"),

    path("enrollments/", views.enrollments_management, name="enrollments"),
    path("enrollments/add/", views.add_enrollment, name="add_enrollment"),
    path("enrollments/<int:pk>/edit/", views.edit_enrollment, name="edit_enrollment"),
    path("enrollments/<int:pk>/delete/", views.delete_enrollment, name="delete_enrollment"),
]
