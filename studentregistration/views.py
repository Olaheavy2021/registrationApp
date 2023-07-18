from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
import requests

from .forms import ContactForm
from .models import Group, Module, Registration
from users.custom_decorators import login_required_message
from studentregistration.utils import get_student_from_request


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
    if "query" in request.GET:
        query = request.GET["query"]
        courses = Group.objects.all()
        courses = courses.filter(name__icontains=query)
    else:
        courses = Group.objects.all()
    all_courses = {"courses": courses, "title": "Our Courses"}
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

    # student will return None if it doesn't exist
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


@login_required_message
@login_required
def student_registrations(request):
    registrations = Registration.objects.filter(student=request.user.student).order_by(
        "registration_date"
    )

    # paginate the registrations
    paginated_registrations = Paginator(registrations, 2)
    page_list = request.GET.get("page")
    paginated_registrations = paginated_registrations.get_page(page_list)
    context = {
        "title": "My Registrations",
        "paginated_registrations": paginated_registrations,
    }
    return render(request, "studentregistration/registrations.html", context)


@login_required_message
@login_required
def register(request, code):
    module = get_object_or_404(Module, code=code)

    # incase user tries to re-register buy copying the register url
    registration, created = Registration.objects.get_or_create(
        module=module, student=request.user.student
    )
    if created:
        messages.success(request, f"Successfully registered to {module.name}")
    else:
        messages.success(request, f"You've already registered to {module.name}")

    # redirect to previous page that sent user here
    # or build the module page url and redirect user there
    module_page = reverse("studentregistration:module_details", args=[module.code])
    redirect_to = request.META.get("HTTP_REFERER", module_page)
    return redirect(redirect_to)


@login_required_message
@login_required
def unregister(request, code):
    registration = get_object_or_404(
        Registration, module__code=code, student=request.user.student
    )
    module = registration.module
    if request.method == "POST":
        registration.delete()
        messages.success(request, f"Successfully unregistered from {module.name}")
        return redirect(
            reverse("studentregistration:module_details", args=[module.code])
        )
        # module_page = reverse("studentregistration:module_details", args=[module.code])
        # redirect_to = request.META.get("HTTP_REFERER", module_page)
        # return redirect(redirect_to)

    context = {"title": "Unregister", "module": module, "registration": registration}
    return render(request, "studentregistration/unregister.html", context)


def error_404(request, exception):
    return render(request, "studentregistration/404.html", {"title": "404 Error"})


@login_required_message
@login_required
def book_list(request):
    if "query" in request.GET:
        query = request.GET["query"]
        print("Search Query " + query)
        url = '{}?q={}&maxResults=10&key={}'
        # Request the API data and convert the JSON to Python data types
        book_data = requests.get(url.format(settings.GOOGLE_BOOKS_API_URL, query,
                                            settings.GOOGLE_API_KEY)).json()
        return render(request, "studentregistration/book_list.html", {"title": "Library", "books": book_data['items']})
    else:
        return render(request, "studentregistration/book_list.html", {"title": "Library"})


@login_required_message
@login_required
def book_details(request, id):
    url = '{}/{}?key={}'
    # Request the API data and confirm the response
    book_data = requests.get(url.format(settings.GOOGLE_BOOKS_API_URL, id, settings.GOOGLE_API_KEY)).json()
    # check if book details is found
    if book_data.get('error'):
        messages.error(request, "Book Details not found")
        return redirect(
            reverse("studentregistration:library")
        )
    else:
        return render(request, "studentregistration/book_details.html", {"title": "Book Details", "book": book_data})
