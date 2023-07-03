from django.shortcuts import render


def login(request):
    return render(request, "users/login.html", {"title": "Sig In"})


def register(request):
    return render(request, "users/register.html", {"title": "Sign Up"})
