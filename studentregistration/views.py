from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import render, get_object_or_404


from .forms import ContactForm
from .models import Group, Module
from studentregistration.utils import get_student_from_request


# Create your views here


def home(request):
    # load the courses from the database
    all_courses = {"courses": Group.objects.all(), "title": "Welcome"}
    return render(request, "studentregistration/home.html", all_courses)


def about(request):
    return render(request, "studentregistration/about.html", {"title": "About US"})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            email = EmailMessage(
                f" CloudGeeks - {form.cleaned_data['name']} - {form.cleaned_data['subject']}",
                form.cleaned_data["message"],
                form.cleaned_data["email"],
                [
                    settings.EMAIL_HOST_USER,
                    "themaleem@gmail.com",
                    "charityodoh75@gmail.com",
                ],
            )

            email.send(fail_silently=False)

            messages.success(request, "Your message has been sent. Thank you!")
            return render(
                request,
                "studentregistration/contact.html",
                {"title": "Contact", "form": ContactForm()},
            )
        else:
            return render(
                request,
                "studentregistration/contact.html",
                {"title": "Contact", "form": form},
            )
    else:
        form = ContactForm()
    return render(
        request, "studentregistration/contact.html", {"title": "Contact", "form": form}
    )


def course_list(request):
    all_courses = {"courses": Group.objects.all(), "title": "Our Courses"}
    return render(request, "studentregistration/course_list.html", all_courses)


def course_details(request, id=1):
    course = Group.objects.get(id=id)
    modules = course.modules.all()
    course_view_details = {
        "course": course,
        "modules": modules,
        "title": "Course Details",
    }
    return render(
        request, "studentregistration/course_details.html", course_view_details
    )


def module_details(request, code):
    module = get_object_or_404(Module, code=code)

    # student will return None if it doesnt't exist
    student = get_student_from_request(request)

    context = {
        "module": module,
        "title": module.name,
        "registrations_count": module.registrations_count,
        "registrations": module.student_registration_details,
    }

    context["can_register"] = student is not None and student.can_register_on_module(
        module
    )

    context[
        "has_registration"
    ] = student is not None and student.has_registered_on_module(module)

    return render(request, "studentregistration/module_details.html", context)


def error_404(request, exception):
    return render(request, "studentregistration/404.html", {"title": "404 Error"})
