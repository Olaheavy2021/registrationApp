from .models import Student


def get_student_from_request(request_object):
    """
    Retrieve the student associated with the authenticated user from the request.

    This function checks if the user in the request is authenticated. If authenticated,
    it attempts to retrieve the corresponding student record from the database.

    Parameters:
    - request_object (HttpRequest): The request object containing a django User Object information.

    Returns:
    - Student instance: if the user is authenticated and has an associated student record.
    - None otherwise.
    """
    if request_object.user.is_authenticated:
        queryset = Student.objects.filter(user=request_object.user)
        return queryset.first() if queryset.exists() else None
    return None
