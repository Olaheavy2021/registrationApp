from django.urls import path
from . import views

app_name = "studentregistration"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("courses", views.course_list, name="course_list"),
    path("module/<slug:code>/register", views.register, name="register"),
    path("course/<int:id>", views.course_details, name="course_details"),
    path("module/<slug:code>", views.module_details, name="module_details"),
    path("module/<int:id>/unregister", views.unregister, name="unregister"),
    path("student/registrations/", views.student_registrations, name="registrations"),
    path("library/books", views.book_list, name="library"),
    path("library/book/<str:id>/", views.book_details, name="book_details"),
    path("student/graduate-jobs/", views.job_list, name="job_list"),
]
