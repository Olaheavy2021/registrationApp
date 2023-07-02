from django.test import TestCase
from django.contrib.auth.models import User


# Create your tests here.


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345', first_name='test', last_name='user')

    def test_user_model(self):
        d = self.user
        self.assertTrue(isinstance(d, User))
        self.assertEqual(str(d), 'testuser')

    def tearDown(self):
        self.user.delete()
