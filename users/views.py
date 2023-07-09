from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login
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
                return redirect("dashboard")
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


def dashboard(request):
    return render(request, "users/dashboard.html", {"title": "Student Dashboard"})


def reset_password(request):
    return render(request, "users/reset_password.html", {"title": "Reset Password"})


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
