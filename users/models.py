from django.db import models
from django.contrib.auth.models import User, Group


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(default="default.png", upload_to="profile_photos")
    course = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} "

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
