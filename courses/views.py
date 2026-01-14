from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Courses
from enrollments.models import Enrollment


@login_required
def courses_list_view(request):
    courses = Courses.objects.filter(is_active=True)

    # Get user's enrollments once
    enrollments = Enrollment.objects.filter(student=request.user)

    # Attach enrollment status to each course
    for course in courses:
        enrollment = enrollments.filter(course=course).first()
        course.enrollment_status = enrollment.status if enrollment else None

    return render(
        request,
        "courses/courses_list.html",
        {"courses": courses}
    )

@login_required
def course_detail_view(request, course_id):
    course = get_object_or_404(Courses, id=course_id, is_active=True)

    enrollment = Enrollment.objects.filter(
        student=request.user,
        course=course
    ).first()

    if request.method == "POST" and enrollment and enrollment.status == "in_progress":
        enrollment.status = "completed"
        enrollment.save()
        return redirect("courses:detail", course_id=course.id)

    context = {
        "course": course,
        "is_enrolled": bool(enrollment),
        "enrollment_status": enrollment.status if enrollment else None,
        "enrollment": enrollment
    }

    return render(request, "courses/course_detail.html", context)
