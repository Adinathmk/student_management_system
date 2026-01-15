# admin_panel/views.py
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from accounts.forms import StudentRegisterForm,StudentUpdateForm
from courses.models import Courses
from enrollments.models import Enrollment
from django.contrib import messages
from courses.models import Courses
from django.db.models import Q
from django.core.paginator import Paginator



from accounts.models import User
from courses.models import Courses
from enrollments.models import Enrollment
from django.contrib.auth.decorators import login_required



@login_required
def admin_dashboard(request):
    
    total_students = User.objects.filter(role="student").count()
    active_courses = Courses.objects.filter(is_active=True).count()
    total_enrollments = Enrollment.objects.count()

   
    recent_students = (
        User.objects
        .filter(role="student")
        .order_by("-date_joined")[:5]
    )

    context = {
        "total_students": total_students,
        "active_courses": active_courses,
        "total_enrollments": total_enrollments,
        "recent_students": recent_students,
    }

    return render(request, "admin/dashboard.html", context)




@login_required
def students_management(request):
    query = request.GET.get("q")

    students = User.objects.filter(role="student")

    if query:
        students = students.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        )

    students = students.order_by("-date_joined")

    # PAGINATION
    paginator = Paginator(students, 5)  # 10 students per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "students": page_obj,     # important
        "page_obj": page_obj,
        "query": query,
    }
    return render(request, "admin/students_management.html", context)



@login_required
def courses_management(request):
    query = request.GET.get("q")

    courses = Courses.objects.all()

    if query:
        courses = courses.filter(
            Q(title__icontains=query) |
            Q(course_code__icontains=query)
        )

    courses = courses.order_by("id")

    return render(request, "admin/courses_management.html", {
        "courses": courses
    })

from django.db.models import Q

@login_required
def enrollments_management(request):
    query = request.GET.get("q")
    status = request.GET.get("status")

    enrollments = Enrollment.objects.select_related(
        "student", "course"
    )

    # 🔍 SEARCH
    if query:
        enrollments = enrollments.filter(
            Q(student__username__icontains=query) |
            Q(student__email__icontains=query) |
            Q(course__title__icontains=query) |
            Q(course__course_code__icontains=query)
        )

    # 🎯 FILTER BY STATUS
    if status:
        enrollments = enrollments.filter(status=status)

    enrollments = enrollments.order_by("-enrolled_at")

    return render(request, "admin/enrollments_management.html", {
        "enrollments": enrollments
    })



# ----------------------------------------------------------ADDING------------------------------------------------------------------------


@login_required
def add_student(request):
    if request.method == "POST":
        form = StudentRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("admin_panel:students")
    else:
        form = StudentRegisterForm()

    return render(request, "admin/add/add_student.html", {
        "form": form
    })

@login_required
def add_course(request):
    if request.method == "POST":
        title = request.POST.get("title")
        course_code = request.POST.get("course_code")
        description = request.POST.get("description")
        duration_minutes = request.POST.get("duration_minutes")
        video_url = request.POST.get("video_url")
        image = request.FILES.get("image")

        if not title or not course_code or not duration_minutes:
            messages.error(request, "Please fill all required fields.")
        else:
            Courses.objects.create(
                title=title,
                course_code=course_code,
                description=description,
                duration_minutes=duration_minutes,
                video_url=video_url,
                image=image,
            )
            messages.success(request, "Course added successfully.")
            return redirect("admin_panel:courses")

    return render(request, "admin/add/add_course.html")


@login_required
def add_enrollment(request):
    students = User.objects.filter(role="student")
    courses = Courses.objects.filter(is_active=True)

    if request.method == "POST":
        student_id = request.POST.get("student")
        course_id = request.POST.get("course")
        status = request.POST.get("status")

        if not student_id or not course_id:
            messages.error(request, "Student and Course are required.")
        else:
            exists = Enrollment.objects.filter(
                student_id=student_id,
                course_id=course_id
            ).exists()

            if exists:
                messages.error(request, "This student is already enrolled in this course.")
            else:
                Enrollment.objects.create(
                    student_id=student_id,
                    course_id=course_id,
                    status=status or "pending"
                )
                messages.success(request, "Student enrolled successfully.")
                return redirect("admin_panel:enrollments")

    context = {
        "students": students,
        "courses": courses,
    }
    return render(request, "admin/add/add_enrollment.html", context)


# ----------------------------------------------------------------EDITING AND DELETING-------------------------------------------------------------
@login_required
def edit_student(request, pk):
    student = User.objects.get(pk=pk, role="student")

    if request.method == "POST":
        form = StudentUpdateForm(
            request.POST,
            request.FILES,
            instance=student
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully.")
            return redirect("admin_panel:students")
    else:
        form = StudentUpdateForm(instance=student)

    return render(request, "admin/edit/edit_student.html", {
        "form": form,
        "student": student
    })

@login_required
def delete_student(request, pk):
    if request.method == "POST":
        student = User.objects.get(pk=pk, role="student")
        student.delete()
        messages.success(request, "Student deleted successfully.")
    return redirect("admin_panel:students")

# ----------------------------

@login_required
def edit_course(request, pk):
    course = Courses.objects.get(pk=pk)

    if request.method == "POST":
        course.title = request.POST.get("title")
        course.course_code = request.POST.get("course_code")
        course.description = request.POST.get("description")
        course.duration_minutes = request.POST.get("duration_minutes")
        course.video_url = request.POST.get("video_url")

        # Update image only if uploaded
        if request.FILES.get("image"):
            course.image = request.FILES.get("image")

        course.save()
        messages.success(request, "Course updated successfully.")
        return redirect("admin_panel:courses")

    return render(request, "admin/edit/edit_course.html", {
        "course": course
    })

@login_required
def delete_course(request, pk):
    if request.method == "POST":
        course = Courses.objects.get(pk=pk)
        course.delete()
        messages.success(request, "Course deleted successfully.")

    return redirect("admin_panel:courses")

# -----------------------------------------------------------------------
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required
def edit_enrollment(request, pk):
    enrollment = Enrollment.objects.select_related(
        "student", "course"
    ).get(pk=pk)

    students = User.objects.filter(role="student")
    courses = Courses.objects.filter(is_active=True)

    old_status = enrollment.status  # ✅ store old status

    if request.method == "POST":
        student_id = request.POST.get("student")
        course_id = request.POST.get("course")
        status = request.POST.get("status")

        # Prevent duplicate enrollment
        exists = Enrollment.objects.exclude(pk=pk).filter(
            student_id=student_id,
            course_id=course_id
        ).exists()

        if exists:
            messages.error(
                request,
                "This student is already enrolled in this course."
            )
        else:
            enrollment.student_id = student_id
            enrollment.course_id = course_id
            enrollment.status = status
            enrollment.save()

            # ✅ SEND EMAIL ONLY WHEN STATUS CHANGES TO "Processing"
            if old_status != "in_progress" and status == "in_progress":
                if enrollment.student.email:
                    send_mail(
                        subject="Your Course Enrollment completed",
                        message=(
                            f"Hi {enrollment.student.username},\n\n"
                            f"Your enrollment for the course "
                            f"'{enrollment.course.title}' is now being processed.\n\n"
                            f"You will be notified once it is completed."
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[enrollment.student.email],
                        fail_silently=False,
                    )

            messages.success(request, "Enrollment updated successfully.")
            return redirect("admin_panel:enrollments")

    return render(request, "admin/edit/edit_enrollment.html", {
        "enrollment": enrollment,
        "students": students,
        "courses": courses,
    })


@login_required
def delete_enrollment(request, pk):
    if request.method == "POST":
        enrollment = Enrollment.objects.get(pk=pk)
        enrollment.delete()
        messages.success(request, "Enrollment deleted successfully.")

    return redirect("admin_panel:enrollments")
