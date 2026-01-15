from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied



from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse


class AdminOnlyMiddleware:
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
        if user.is_authenticated and not user.is_active:
            logout(request)
            messages.error(
                request,
                "Your account is inactive. Please contact the administrator."
            )
            return redirect("login") 

        response = self.get_response(request)
        return response
