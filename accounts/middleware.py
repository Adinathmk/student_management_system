from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied



from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse


class AdminOnlyMiddleware:
    """
    Allows access to admin-panel URLs only for admin users.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/admin/"):

            if not request.user.is_authenticated:
                return redirect("login")

            if not (
                request.user.is_staff or
                getattr(request.user, "role", "") == "admin"
            ):
                raise PermissionDenied

        return self.get_response(request)
    



class IsActiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        # Check only if user is logged in
        if user.is_authenticated and not user.is_active:
            logout(request)
            messages.error(
                request,
                "Your account is inactive. Please contact the administrator."
            )
            return redirect(reverse("login"))  # change if login url name differs

        response = self.get_response(request)
        return response
