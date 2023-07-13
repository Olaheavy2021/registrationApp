from .models import Student


def get_student_from_request(request_object):
    if request_object.user.is_authenticated:
        queryset = Student.objects.filter(user=request_object.user)
        if queryset.exists():
            return queryset.first()
        else:
            return None
    else:
        return None
