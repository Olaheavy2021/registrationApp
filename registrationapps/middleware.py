from django.urls import reverse
from django.shortcuts import redirect


class RedirectLoggedInMiddleware:
    """
    Custom Middleware to redirect authenticated users who attempt to
    access the login or register pages to the dashboard.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # if the user is authenticated
        # and if the current page is login or register pages
        if request.user.is_authenticated and request.path in [
            reverse("login"),
            reverse("register"),
        ]:
            # Redirect the user to the dashboard
            return redirect("dashboard")

        response = self.get_response(request)
        return response
