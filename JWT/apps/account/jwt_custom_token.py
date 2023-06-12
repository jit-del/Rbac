from rest_framework_simplejwt.tokens import RefreshToken
import random


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


def generate_otp():
    otp = random.randint(100000, 999999)
    return otp
