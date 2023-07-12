from django.test import TestCase
from django.contrib.auth.models import User, Group
from .models import Student


# Create your tests here.


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="12345", first_name="test", last_name="user"
        )

    def test_user_model(self):
        d = self.user
        self.assertTrue(isinstance(d, User))
        self.assertEqual(str(d), "testuser")

    def tearDown(self):
        self.user.delete()


class StudentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="12345", first_name="test", last_name="user"
        )
        self.course = Group.objects.create(name="Test course")
        self.student = Student.objects.create(
            user=self.user, dob="2000-01-01", address="test address", city="test city", country="test country",
            course=self.course
        )

    def test_student_model(self):
        d = self.student
        self.assertTrue(isinstance(d, Student))
        self.assertEqual(str(d), "test user")

    def tearDown(self):
        self.student.delete()
        self.user.delete()
