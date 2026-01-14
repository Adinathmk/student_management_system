from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from courses.models import Courses
from .models import Enrollment


@login_required
def enroll_course_view(request, course_id):

    course = get_object_or_404(Courses, id=course_id, is_active=True)

    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        course=course
    )

    if created:
        send_mail(
            subject="New Course Enrollment",
            message=(
                f"A new student has enrolled.\n\n"
                f"Student: {request.user.username}\n"
                f"Email: {request.user.email}\n"
                f"Course: {course.title}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER], 
            fail_silently=False,
        )
        messages.success(request, "Successfully enrolled in course!")
    else:
        messages.info(request, "You are already enrolled in this course.")

    return redirect("courses:detail", course_id=course.id)
