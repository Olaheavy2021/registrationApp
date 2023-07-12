from django.contrib import messages
from .forms import CustomPasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from .models import Student
from .forms import (
    StudentRegistrationForm,
    CustomLoginForm,
    UserUpdateForm,
    ProfileUpdateForm,
)


def login_view(request):
    if request.method == "POST":
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
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
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
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
        form = StudentRegistrationForm()

    context = {"title": "Sign Up", "form": form}
    return render(request, "users/register.html", context)


@login_required
def dashboard(request):
    return render(request, "users/dashboard.html", {"title": "Student Dashboard"})


@login_required
def profile(request):
    if request.method == "POST":
        # Handle form submission
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.student
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile was successfully updated")
            return redirect("profile")
        else:
            messages.warning(request, "Profile could not be updated!")
    else:
        # Display the profile form
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.student)
    context = {"u_form": u_form, "p_form": p_form, "title": "Student Profile"}
    return render(request, "users/profile.html", context)


class CustomLogoutView(LogoutView):
    next_page = "studentregistration:home"


@login_required
def change_password(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(
                request, user
            )  # Important, to update the session with the new password
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
