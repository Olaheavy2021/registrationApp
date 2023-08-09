from datetime import datetime
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login
from django.contrib.auth import update_session_auth_hash

from .models import Student, User
from .forms import CustomPasswordChangeForm
from studentregistration.models import Registration
from .forms import (
    CustomLoginForm,
    UserUpdateForm,
    ProfileUpdateForm,
    UserStudentRegistrationForm,
)
from .custom_decorators import login_required_with_message, redirect_if_admin


def login_view(request):
    """
    View function for handling user login.
    """
    if request.method == "POST":
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            # Check if user exists and is authenticated
            if user is not None:
                login(request, user)
                messages.success(request, "Successfully logged in")
                # Retrieve the 'next' parameter or dashboard
                redirect_to = request.GET.get("next", "dashboard")
                return redirect(redirect_to)
            else:
                messages.warning(request, "Unable to  login!")
    else:
        form = CustomLoginForm()

    return render(request, "users/login.html", {"title": "Sign In", "form": form})


def register(request):
    """
    View function for registering a new student user.
    """
    if request.method == "POST":
        form = UserStudentRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            # Check if email already exists
            if User.objects.filter(email=email).exists():
                messages.warning(request, "Email address already exists!")
            else:
                # Create user and student objects and save to the database
                user = form.save(commit=False)
                student = Student(
                    user=user,
                    course=form.cleaned_data["course"],
                )
                user.save()
                student.save()
                messages.success(
                    request, "Your account has been created! Now you can login!"
                )
                # Redirect to login page on success
                return redirect("login")

        else:
            messages.warning(request, "Unable to create account!")
    else:
        form = UserStudentRegistrationForm()

    context = {"title": "Sign Up", "form": form}
    return render(request, "users/register.html", context)


@login_required_with_message
@redirect_if_admin
def dashboard(request):
    # Get the modules for the courses
    course = request.user.student.course
    modules = course.modules.all().order_by("name")

    # Get the registrations for the student
    registrations = Registration.objects.filter(student=request.user.student)

    # paginate the modules
    paginated_modules = Paginator(modules, 2)
    page_list = request.GET.get("page")
    paginated_modules = paginated_modules.get_page(page_list)
    context = {
        "title": "Student Dashboard",
        "modules": modules,
        "registrations": registrations,
        "paginated_modules": paginated_modules,
    }
    return render(request, "users/dashboard.html", context)


@login_required_with_message
@redirect_if_admin
def profile(request):
    """
    View function to display and update the user's profile.
    """
    user = request.user
    if request.method == "POST":
        # Handle form submission
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.student)
        date = datetime.strptime(p_form.data["dob"], "%Y-%m-%d")
        if date.date() > timezone.localtime(timezone.now()).date():
            messages.error(request, "Date of birth cannot be in the future!")
            context = {"u_form": u_form, "p_form": p_form, "title": "Student Profile"}
            return render(request, "users/profile.html", context)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile was successfully updated")
            return redirect("profile")
        else:
            messages.warning(request, "Profile could not be updated!")
    else:
        # Display the profile form
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=user.student)
    context = {"u_form": u_form, "p_form": p_form, "title": "Student Profile"}
    return render(request, "users/profile.html", context)


class CustomLogoutView(LogoutView):
    """
    Custom view to handle user logout and redirect to home page.
    """

    next_page = "studentregistration:home"


@login_required_with_message
def change_password(request):
    """
    View function to handle password change for logged-in users.
    """
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # update the session with the new password
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("dashboard")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(
        request,
        "users/change_password.html",
        {"form": form, "title": "Change Password"},
    )
