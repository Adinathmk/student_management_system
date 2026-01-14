from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from enrollments.models import Enrollment


@login_required
def profile_view(request):
    user = request.user

    if request.method == "POST":
        user.email = request.POST.get("email", user.email)
        user.phone = request.POST.get("phone", user.phone)
        user.gender = request.POST.get("gender", user.gender)
        user.date_of_birth = request.POST.get("date_of_birth", user.date_of_birth)

        if request.FILES.get("profile_picture"):
            user.profile_picture = request.FILES["profile_picture"]

        user.save()
        return redirect("students:profile")

    return render(request, "students/profile.html")



@login_required
def student_dashboard_view(request):

    enrollments = Enrollment.objects.filter(student=request.user)

    context = {
        "enrollments": enrollments,
        "enrolled_count": enrollments.count(),
        "in_progress_count": enrollments.filter(status="in_progress").count(),
        "completed_count": enrollments.filter(status="completed").count(),
    }

    return render(request, "students/dashboard.html", context)

