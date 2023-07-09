from django.db import models
from users.models import Student, Group


class Module(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)
    credit = models.IntegerField()
    category = models.CharField(max_length=255)
    description = models.TextField()
    available = models.BooleanField(default=True)
    courses = models.ManyToManyField(Group, related_name="modules")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Module"
        verbose_name_plural = "Modules"


class Registration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.module.name}"

    class Meta:
        verbose_name = "Registration"
        verbose_name_plural = "Registrations"
