from django.urls import re_path
from apps.account import views
from rest_framework import routers
router = routers.SimpleRouter()
router.register(
    "profile", views.UserProfileAPIView
)

app_name = "account"

urlpatterns = [
    re_path(r"user-register/$", views.CreateUserAPIView.as_view()),
    re_path(r"send-otp/$", views.UserOtpAPIView.as_view()),
    re_path(r"login-verify/$", views.UserLoginAPIView.as_view()),
    re_path(r"change-password/$", views.UserChangePasswordAPIView.as_view()),
    re_path(r"send-reset-password-link/$", views.UserResetPasswordEmailLinkAPIView.as_view()),
    re_path(r"reset-password/<uid>/<token>/$", views.UserResetPasswordAPIView.as_view()),  
]+ router.urls
