from django.shortcuts import render

# Create your views here


def home(request):
    return render(request, "studentregistration/home.html", {"title": "Welcome"})


def about(request):
    return render(request, "studentregistration/about.html", {"title": "About US"})


def contact(request):
    return render(request, "studentregistration/contact.html", {"title": "Contact"})
