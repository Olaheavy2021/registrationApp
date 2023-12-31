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
        """
        String representation of a Student
        """
        return f"{self.user.first_name} {self.user.last_name}"

    def has_registered_on_module(self, module):
        return self.registrations.filter(module=module).exists()

    # note: we check if module is related to the student's course
    def can_register_on_module(self, module):
        return module.is_related_to_student_course(self)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
