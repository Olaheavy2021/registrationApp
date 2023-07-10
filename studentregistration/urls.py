from django.urls import path
from . import views

app_name = "studentregistration"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("courses", views.course_list, name="course_list"),
    path("course/<int:id>", views.course_details, name="course_details"),
    path("modules/detail/<str:code>", views.module_details, name="module_details"),
]
