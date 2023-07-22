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

    custom `POST` action payload data schema example

    `{`
        `"user": {`
            `"username": "C2065612",`
            `"email": "c2065612@cloudgeek.com",`
            `"first_name": "Azeez",`
            `"last_name": "Bello",`
            `"password": "qwertyuiop"`
        `},`
        `"address": "123 Example Street",`
        `"city": "Example City",`
        `"country": "Example Country",`
        `"photo": "example.png",`
        `"course": "example_course_name"`
    `}`

    """

    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    name = "student-list"
    permission_classes = [IsOwnerOrAdmin]

    # overloading the default create() method to add custom workflow
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
            # transaction block to ensure user AND student objects gets created
            # or rollback if errors occur fails
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
                # delete user object if any error occurs
                user.delete()
                raise e
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    An APIView that provides default GET, PATCH, PUT and DELETE actions.
    """

    # @note we need this because of our custom lookup_field on Student

    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    # fetch using username (student_id) instead of django's default pk lookup
    lookup_field = "user__username"
    lookup_url_kwarg = "username"
    name = "student-detail"
    permission_classes = [IsOwnerOrAdmin]


class ModuleViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides default `create()`, `list()`, and `retrieve()` actions.

    custom `POST` action payload data schema example

    `{`
        `"name": "Module Name",`
       `"code": "MODULE1",`
        `"credit": 30,`
        `"category": "Elective",`
        `"description": "Module description",`
        `"available": true,`
        `"courses": [`
            `Course Name 1,`
            `Course Name 2,`
            `...]`
    `}`
    """

    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    name = "module"
    permission_classes = [IsAdminUserOrReadOnly]

    # overloading the default create() method to add custom workflow
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
    """
    An APIView that provides default GET, PATCH, PUT and DELETE actions.
    """

    # @note we need this because of our custom lookup_field on Module
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    lookup_field = "code"
    name = "module-detail"
    permission_classes = [IsAdminUserOrReadOnly]


class CourseViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides default `create()`, `list()`, and `retrieve()` actions.
    """

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
    """
    A viewset that provides default `create()`, `list()`, and `retrieve()` actions.
    """

    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    name = "registration"
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        student_id = request.data.get("student_id")
        module_code = request.data.get("module_code")

        try:
            student = Student.objects.get(user__username=student_id)
            module = Module.objects.get(code=module_code)
        except (Student.DoesNotExist, Module.DoesNotExist):
            return Response(
                {"error": "Invalid student ID or module code"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        registration_data = {"student": student.id, "module": module.id}

        serializer = self.get_serializer(data=registration_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RegistrationDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    A APIView that provides default GET, PUT, PATCH, DELETE actions.
    """

    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    name = "registration-detail"
    permission_classes = [IsOwnerOrAdmin]
