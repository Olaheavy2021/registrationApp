from django.db import models
from users.models import Student
from django.contrib.auth.models import Group


class Module(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)
    credit = models.IntegerField()
    category = models.CharField(max_length=255)
    description = models.TextField()
    available = models.BooleanField(default=True)
    # course = models.ManyToManyField(Group, on_delete=models.CASCADE)


class Registration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    registration_date = models.DateField(auto_now_add=True)
