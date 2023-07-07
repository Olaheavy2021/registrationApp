from django.shortcuts import render
from .forms import ContactForm
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Group

# Create your views here


def home(request):
    all_courses = {'courses': Group.objects.all(), "title": "Welcome"}
    return render(request, "studentregistration/home.html", all_courses)


def about(request):
    return render(request, "studentregistration/about.html", {"title": "About US"})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            email = EmailMessage(
                f" CloudGeeks - {form.cleaned_data['name']} - {form.cleaned_data['subject']}",
                form.cleaned_data['message'],
                form.cleaned_data['email'],
                [settings.EMAIL_HOST_USER, 'themaleem@gmail.com', 'charityodoh75@gmail.com']
            )

            email.send(fail_silently=False)

            messages.success(request, 'Your message has been sent. Thank you!')
            return render(request, 'studentregistration/contact.html', {'title': 'Contact', 'form': ContactForm()})
        else:
            return render(request, 'studentregistration/contact.html', {'title': 'Contact', 'form': form})
    else:
        form = ContactForm()
    return render(request, "studentregistration/contact.html", {"title": "Contact", 'form': form})
