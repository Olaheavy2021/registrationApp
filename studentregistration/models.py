from django.db import models
from users.models import Student, Group


class Module(models.Model):
    CategoryChoice = (("Elective", "Elective"), ("Compulsory", "Compulsory"))
    name = models.CharField(max_length=255, null=False)
    code = models.SlugField(max_length=12, default="", null=False, unique=True)
    credit = models.IntegerField(null=False)
    category = models.CharField(max_length=255, choices=CategoryChoice, null=False)
    description = models.TextField(null=False)
    available = models.BooleanField(default=True, null=False)
    courses = models.ManyToManyField(Group, related_name="modules")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Module"
        verbose_name_plural = "Modules"

    @property
    def attached_courses(self):
        return self.courses.all()

    @property
    def registered_students(self):
        return [registration.student for registration in self.registrations.all()]

    @property
    def student_registration_details(self):
        return [
            {"student": registration.student, "date": registration.registration_date}
            for registration in self.registrations.all()
        ]

    @property
    def registrations_count(self):
        return self.registrations.count()

    # we filter courses on this current module by a specific student object
    # if we get a match, then we know the student can register for the module
    def is_related_to_student_course(self, student):
        return self.courses.filter(student=student).exists()


class Registration(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="registrations"
    )
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name="registrations"
    )
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.module.name}"

    class Meta:
        verbose_name = "Registration"
        verbose_name_plural = "Registrations"
        constraints = [
            models.UniqueConstraint(
                fields=["student", "module"], name="unique_registration"
            )
        ]
