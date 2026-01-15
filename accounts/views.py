from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .forms import StudentRegisterForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.conf import settings




def register_view(request):
    if request.method == "POST":
        form = StudentRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            try:
                send_mail(
                    subject="Welcome to Our Platform",
                    message="Hi {},\n\nYour registration was successful.\n\nThank you!".format(user.username),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print("Email error:", e)

            messages.success(request, "Registration successful. Please login.")
            return redirect("login")
    else:
        form = StudentRegisterForm()
        form.fields.pop("is_active", None)

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            if not user.is_active:
                messages.error(request, "Your account is inactive. Please contact admin.")
                return redirect("login")

            login(request, user)
            messages.success(request, "Login successful")

            if user.is_staff or user.role == "admin":
                return redirect("admin_panel:dashboard")

            return redirect("students:dashboard")

    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect('login')

