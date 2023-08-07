from django.contrib import admin
from studentregistration.models import Module, Registration, Job


# Register amodels on admin page

admin.site.register(Job)
admin.site.register(Module)
admin.site.register(Registration)
