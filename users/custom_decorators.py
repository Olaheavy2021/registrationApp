from functools import wraps

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib import messages

default_message = "You do not have permission to view this page. Please login first."


def custom_user_passes_test(
        test_func, message=default_message
):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not test_func(request.user):
                messages.error(request, message)
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def login_required_message(
        function=None,
        message=default_message
):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = custom_user_passes_test(
        lambda u: u.is_authenticated,
        message=message,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
