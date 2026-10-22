import logging

from django.urls import path
from django.http import JsonResponse
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver

security_logger = logging.getLogger("secureapp.security")


@receiver(user_logged_in)
def log_successful_login(sender, request, user, **kwargs):
    security_logger.info(
        "Successful login: username=%s ip=%s",
        user.get_username(),
        request.META.get("REMOTE_ADDR", "unknown"),
    )


@receiver(user_login_failed)
def log_failed_login(sender, credentials, request, **kwargs):
    username = credentials.get("username", "unknown")
    ip = request.META.get("REMOTE_ADDR", "unknown") if request else "unknown"

    security_logger.warning(
        "Failed login attempt: username=%s ip=%s",
        username,
        ip,
    )


def health(request):
    return JsonResponse({
        "status": "ok",
        "service": "secureapp",
    })


@login_required
def dashboard(request):
    return JsonResponse({
        "message": "Authentication successful",
        "user": request.user.username,
    })


urlpatterns = [
    path("health/", health, name="health"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path("dashboard/", dashboard, name="dashboard"),
]
