import requests
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .forms import ContactForm
from .models import Group, Module, Registration, Job
from studentregistration.utils import get_student_from_request
from users.custom_decorators import login_required_with_message, redirect_if_admin


def home(request):
    # load the courses from the database
    all_courses = {
        "title": "Welcome",
        "courses": Group.objects.all(),
    }
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
                settings.RECIPIENTS,
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
    # Fetch the query parameter from the request or set it to an empty string as default.
    query = request.GET.get("query", "")
    courses = Group.objects.all()

    # If there's a query, filter courses based on the query.
    if query:
        courses = courses.filter(name__icontains=query)
    context = {
        "query": query,
        "courses": courses,
        "title": "Our Courses",
    }
    return render(request, "studentregistration/course_list.html", context)


def course_details(request, id):
    """
    Render details of a specific course by it's ID

    Parameters:
    - request (HttpRequest): The request object containing user and other metadata.
    - id (int): The unique identifier of the course (Group) for which details are to be fetched.

    Returns:
    - HttpResponse: A rendered HTML page showing the details of the specified course.
    """

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
    """
    Render details of a specific module by it's code

    Parameters:
    - request (HttpRequest): The request object containing user and other metadata.
    - code (string): The unique identifier of the module for which details are to be fetched.

    Returns:
    - HttpResponse: A rendered HTML page showing the details of the specified module.
    """
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


@login_required_with_message
@redirect_if_admin
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


@login_required_with_message
@redirect_if_admin
def register(request, code):
    """
    Register a student for a specific module.

    If the student has already registered for the module, a message is shown indicating that.

    Parameters:
    - request (HttpRequest): The request object containing user and other metadata.
    - code (str): The unique code identifier of the module.

    Returns:
    - HttpResponse: Redirects the user to the relevant page with a success message.
    """
    module = get_object_or_404(Module, code=code)
    # incase user tries to re-register buy visiting the register url
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


@login_required_with_message
@redirect_if_admin
def unregister(request, id):
    """
    Unregister a student from a specific module.

    Given the ID of a module, this function checks if the logged-in student
    is registered for the module and, if so, unregisters the student by deleting the corresponding
    registration record. A success message is then displayed to the user.

    Parameters:
    - request (HttpRequest): The request object containing user and other metadata.
    - id (int): The unique identifier of the module (Registration) the student wants to unregister from.

    Returns:
    - HttpResponse: Redirects the user to the module's details page with a success message.
    """
    registration = get_object_or_404(
        Registration, module__id=id, student=request.user.student
    )
    module = registration.module
    registration.delete()
    messages.success(request, f"Successfully unregistered from {module.name}")

    # redirect to previous page that sent user here
    # or build the module page url and redirect user there
    module_page = reverse("studentregistration:module_details", args=[module.code])
    redirect_to = request.META.get("HTTP_REFERER", module_page)
    return redirect(redirect_to)


def error_404(request, exception):
    return render(request, "studentregistration/404.html", {"title": "404 Error"})


@login_required_with_message
def book_list(request):
    """
    Display a list of books based on a search query.

    This view function fetches book information from the Google Books API based on a search query
    provided. If no query is provided, render a page where logged in users can
    search for books.
    """
    query = request.GET.get("query", "")

    context = {"title": "Library", "query": query}
    # Request the API data and convert the JSON to Python data types
    if query:
        url = "{}?q={}&maxResults=10&key={}"
        book_data = requests.get(
            url.format(settings.GOOGLE_BOOKS_API_URL, query, settings.GOOGLE_API_KEY)
        ).json()
        context["books"] = book_data.get("items", [])

    return render(request, "studentregistration/book_list.html", context)


@login_required_with_message
def book_details(request, id):
    """
    Fetch and display details of a specific book based on its ID.

    This view function queries the Google Books API for detailed information about a book
    identified by its ID. It renders a page showing the information if the book is found.
    Otherwise, it redirects the user to the library page with an error message.

    Parameters:
    - request (HttpRequest): The request object containing user data and other metadata.
    - id (str): The unique identifier of the book to fetch details for.

    Returns:
    - HttpResponse: Either a rendered HTML page showing the book details or a redirect to the library page.
    """

    # Format the API endpoint URL using the book ID and API key.
    url = "{}/{}?key={}"
    book_data = requests.get(
        url.format(settings.GOOGLE_BOOKS_API_URL, id, settings.GOOGLE_API_KEY)
    ).json()

    # Check if the API response contains an error indicating that the book's details were not found.
    if book_data.get("error"):
        messages.error(request, "Book Details not found")
        return redirect(reverse("studentregistration:library"))

    # If no error is present in the response, render the book details page with the fetched data.
    return render(
        request,
        "studentregistration/book_details.html",
        {"title": "Book Details", "book": book_data},
    )


@login_required_with_message
def job_list(request):
    jobs = Job.objects.all()
    # paginate the registrations
    paginated_jobs = Paginator(jobs, 5)
    page_list = request.GET.get("page")
    paginated_jobs = paginated_jobs.get_page(page_list)
    return render(
        request,
        "studentregistration/job_list.html",
        {"title": "Graduate Jobs", "paginated_jobs": paginated_jobs},
    )
