from django.contrib import messages
from django.shortcuts import render, redirect

# from django.views.generic.edit import CreateView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login

from .models import Student
from .forms import StudentRegistrationForm, CustomLoginForm

from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomPasswordChangeForm


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


def profile(request):
    return render(request, "users/profile.html", {"title": "Student Profile"})


def reset_password(request):
    return render(request, "users/reset_password.html", {"title": "Reset Password"})


class CustomLogoutView(LogoutView):
    next_page = "studentregistration:home"

def reset_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important, to update the session with the new password
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'users/reset_password.html', {'form': form})