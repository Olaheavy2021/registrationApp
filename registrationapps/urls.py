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

from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

import users.views
from users import views as user_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("studentregistration.urls")),
    path("login/", user_views.login_view, name="login"),
    path("register", user_views.register, name="register"),
    path("logout/", user_views.CustomLogoutView.as_view(), name="logout"),
    path("student/dashboard/", users.views.dashboard, name="dashboard"),
    path("student/profile/", users.views.profile, name="profile"),
    path("student/change-password/", users.views.change_password, name="change_password"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
