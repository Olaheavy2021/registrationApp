from django.db import transaction
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import permissions, generics, viewsets, status

from users.models import Student
from studentregistration.models import Module, Group, Registration
from .serializers import (
    StudentSerializer,
    UserSerializer,
    ModuleSerializer,
    CourseSerializer,
    RegistrationSerializer,
)
from registrationapps.permissions import IsAdminUserOrReadOnly, IsOwnerOrAdmin


class StudentViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides default `create()`, `list()`, and `retrieve()` actions.
    """

    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    name = "student-list"
    permission_classes = [IsOwnerOrAdmin]

    def create(self, request, *args, **kwargs):
        course_name = request.data.get("course")
        course = Group.objects.get(name=course_name)

        user_data = request.data.get("user")
        student_data = request.data.copy()
        student_data.pop("user", None)
        student_data["course"] = course

        user_serializer = UserSerializer(data=user_data)

        # initialize a user object
        user = None
        if user_serializer.is_valid():
            try:
                with transaction.atomic():
                    user = user_serializer.save()
                    student_serializer = StudentSerializer(data=student_data)
                    if student_serializer.is_valid():
                        student = Student.objects.create(
                            user=user, **student_data, course=course
                        )
                        response_serializer = StudentSerializer(student)
                        return Response(
                            response_serializer.data, status=status.HTTP_201_CREATED
                        )
                    else:
                        raise serializers.ValidationError(student_serializer.errors)
            except Exception as e:
                # delete use object if any error occurs
                user.delete()
                raise e
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = "user__username"
    lookup_url_kwarg = "username"
    name = "student-detail"
    permission_classes = [IsOwnerOrAdmin]


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    name = "module"
    permission_classes = [IsAdminUserOrReadOnly]

    def create(self, request, *args, **kwargs):
        courses_data = request.data.pop("courses", [])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        module = serializer.save()

        if courses_data:
            courses = Group.objects.filter(name__in=courses_data)
            module.courses.set(courses)

        response_serializer = self.get_serializer(module)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class ModuleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    lookup_field = "code"
    name = "module-detail"
    permission_classes = [IsAdminUserOrReadOnly]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = CourseSerializer
    name = "course"
    permission_classes = [IsAdminUserOrReadOnly]


# @note we might use this for course details lookup by course name
# class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Group.objects.all()
#     serializer_class = CourseSerializer
#     lookup_field = "name"
#     name = "course-detail"
#     permission_classes = [IsAdminUserOrReadOnly]


# @todo  review permissions
class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    name = "registration"
    permission_classes = [permissions.IsAuthenticated]


class RegistrationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    name = "module-detail"
    permission_classes = [IsOwnerOrAdmin]
