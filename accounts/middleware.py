from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

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
