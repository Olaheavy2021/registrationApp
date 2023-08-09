from django.urls import reverse
from rest_framework import serializers


from .models import Student, Group, User
from studentregistration.models import Module, Registration, Job


class UsernameHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    """
    Custom field to generate hyperlinks based on usernames rather than primary keys.
    """

    def to_representation(self, value):
        # Constructs the hyperlink using the user's username
        username = value.user.username
        request = self.context.get("request")
        kwargs = {self.lookup_field: username}
        path = reverse(self.view_name, kwargs=kwargs)
        return request.build_absolute_uri(path)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Student model, including related fields from the User model.
    """

    course = serializers.SlugRelatedField(
        queryset=Group.objects.all(), slug_field="name"
    )
    email = serializers.ReadOnlyField(source="user.email")
    student_id = serializers.ReadOnlyField(source="user.username")
    url = UsernameHyperlinkedIdentityField(
        view_name="student-detail", lookup_field="username"
    )

    class Meta:
        model = Student
        fields = [
            "url",
            "student_id",
            "email",
            "address",
            "city",
            "country",
            "photo",
            "course",
        ]


class StudentRegistrationDetailsSerializer(serializers.Serializer):
    """
    Serializer for showing registration details of a student.
    """

    student = serializers.CharField()
    date = serializers.DateTimeField()


class ModuleSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Module model with related course data and student registration details.
    """

    courses = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    url = serializers.HyperlinkedIdentityField(
        view_name="module-detail", lookup_field="code"
    )
    student_registration_details = StudentRegistrationDetailsSerializer(
        many=True, read_only=True
    )

    class Meta:
        model = Module
        fields = [
            "url",
            "name",
            "code",
            "credit",
            "category",
            "description",
            "available",
            "courses",
            "student_registration_details",
        ]


class CourseModules(serializers.HyperlinkedModelSerializer):
    """
    Serializer for displaying modules related to a course.
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="module-detail", lookup_field="code"
    )

    class Meta:
        model = Module

        fields = [
            "url",
            "name",
        ]


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Course (Group) model including related module data.
    """

    modules = CourseModules(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ["url", "id", "name", "modules"]


class ModuleRegistrationSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for displaying module details in registration.
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="module-detail", lookup_field="code"
    )

    class Meta:
        model = Module
        fields = ["url", "name", "code", "credit"]


class StudentRegistrationSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for displaying student details in registration.
    """

    course = serializers.SlugRelatedField(
        queryset=Group.objects.all(), slug_field="name"
    )
    student_id = serializers.ReadOnlyField(source="user.username")
    url = UsernameHyperlinkedIdentityField(
        view_name="student-detail", lookup_field="username"
    )

    class Meta:
        model = Student
        fields = ["url", "student_id", "course"]


class RegistrationSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Registration model, including related student and module data.
    """

    student_id = serializers.PrimaryKeyRelatedField(
        source="student.user.username",
        read_only=True,
    )
    module_code = serializers.SlugRelatedField(
        slug_field="code",
        source="module",
        read_only=True,
    )

    class Meta:
        model = Registration
        fields = ["url", "id", "student_id", "module_code", "registration_date"]


class JobSerializer(serializers.ModelSerializer):
    """
    Simple serializer for the Job model, including all its fields.
    """

    class Meta:
        model = Job
        fields = "__all__"
