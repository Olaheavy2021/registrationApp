"""
URL configuration for registrationapps project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from drf_yasg import openapi
from django.contrib import admin
from django.conf import settings
from rest_framework import routers
from django.urls import path, include
from drf_yasg.views import get_schema_view
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


from users import views as user_views
from users import api_views as api_views


router = routers.DefaultRouter()
router.register(r"modules", api_views.ModuleViewSet)
router.register(r"courses", api_views.CourseViewSet)
router.register(r"students", api_views.StudentViewSet)
router.register(r"registrations", api_views.RegistrationViewSet)

# API documentation URLs
schema_view = get_schema_view(
    openapi.Info(
        title="Your API Title",
        default_version="v1",
        description="Your API Description",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("studentregistration.urls")),
    path("login/", user_views.login_view, name="login"),
    path("register", user_views.register, name="register"),
    path("student/profile/", user_views.profile, name="profile"),
    path("student/dashboard/", user_views.dashboard, name="dashboard"),
    path("logout/", user_views.CustomLogoutView.as_view(), name="logout"),
    path(
        "student/change-password/", user_views.change_password, name="change_password"
    ),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password_reset_confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("api/", include(router.urls)),
    path(
        "api/student/<str:username>",
        api_views.StudentDetail.as_view(),
        name=api_views.StudentDetail.name,
    ),
    path(
        "api/module/<str:code>",
        api_views.ModuleDetail.as_view(),
        name=api_views.ModuleDetail.name,
    ),
    # path(
    #     "api/course/<str:name>",
    #     CourseDetail.as_view(),
    #     name=CourseDetail.name,
    # ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = "studentregistration.views.error_404"