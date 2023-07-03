from django.db import models
from django.contrib.auth.models import User, Group


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="profile_photos")
    course = models.ForeignKey(Group, on_delete=models.CASCADE)
