from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

default_message = "You do not have permission to view this page. Please login first."


def login_required_with_message(
    function=None, message=default_message, login_url=None, redirect_field_name="next"
):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test is a callable
    that takes the user object and returns True if the user passes.

    """
    actual_decorator = login_required(
        login_url=login_url, redirect_field_name=redirect_field_name
    )

    @wraps(function)
    def wrapped_function(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, message)
        return function(request, *args, **kwargs)

    decorated_function = actual_decorator(wrapped_function)

    return decorated_function


def redirect_if_admin(function):
    """
    View decorator to redirect admin to the admin page if they visit some student specific pages.
    """

    @wraps(function)
    def wrapped_function(request, *args, **kwargs):
        if (
            request.user.is_staff or request.user.is_superuser
        ):  # Check if the user is an admin
            messages.error(request, "You can not see the page as an admin.")
            return redirect("/admin/")  # Redirect to admin site
        return function(request, *args, **kwargs)

    return wrapped_function
