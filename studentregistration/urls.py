from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "studentregistration"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("courses", views.course_list, name="course_list"),
    path("course/<int:id>", views.course_details, name="course_details")
]
