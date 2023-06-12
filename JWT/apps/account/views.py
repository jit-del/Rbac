from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.account.models import User, Otp, UserProfile
from apps.account.serializers import UserRegisterSerializer, LoginSerializers, UserChangePasswordSerializer, UserProfileSerializer, SendPasswordResetLinkEmailSerializer,ResetPasswordSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import generics, status
from apps.account.jwt_custom_token import get_tokens_for_user, generate_otp
from apps.account.sendgrid import SendGrid
from django.contrib.auth import authenticate
from rest_framework.viewsets import ModelViewSet


# Create your views here.
class CreateUserAPIView(APIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            tokens = get_tokens_for_user(user=user)
            return Response(
                status=status.HTTP_201_CREATED,
                data={
                    "error": False,
                    "data": serializer.data,
                    "token": tokens,
                    "message": "User has been successfully registered.",
                },
            )
        return Response(
            status=status.HTTP_204_NO_CONTENT,
            data={
                "error": True,
                "data": serializer.errors,
                "message": "User register failed",
            },
        )


class UserOtpAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        user_obj = User.objects.filter(email=email).values_list("id", flat=True)
        if user_obj:
            instant_otp = generate_otp()
            Otp.objects.get_or_create(user_id=user_obj[0], otp=instant_otp)
            response = SendGrid().send_email_to_user_for_otp_login(
                email=email, otp=instant_otp
            )
            if response in [200, 201, 202]:
                return Response(
                    status=status.HTTP_200_OK,
                    data={
                        "error": True,
                        "message": "Otp send to your email please check",
                    },
                )
        return Response(
            status=status.HTTP_204_NO_CONTENT,
            data={
                "error": True,
                "message": "email is not available please register first",
            },
        )


class UserLoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = request.data.get("email")
            password = request.data.get("password")
            type = request.data.get("type")
            otp = request.data.get("otp")

            if type == "U&P":
                user = authenticate(email=email, password=password)
                if user is None:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={
                            "error": True,
                            "message": "Email or password is not valid",
                        },
                    )

                tokens = get_tokens_for_user(user=user)
                return Response(
                    status=status.HTTP_201_CREATED,
                    data={
                        "error": False,
                        "data": serializer.data,
                        "token": tokens,
                        "message": "User has been successfully registered.",
                    },
                )
            elif type == "OTP":
                if otp and otp != "":
                    db_otp = Otp.objects.filter(user__email=email, otp=otp).values_list(
                        "otp", flat=True
                    )
                    if int(db_otp[0]) == int(otp):
                        user = User.objects.get(email=email)
                        tokens = get_tokens_for_user(user=user)
                        return Response(
                            status=status.HTTP_201_CREATED,
                            data={
                                "error": False,
                                "data": serializer.data,
                                "token": tokens,
                                "message": "User has been successfully logedin.",
                            },
                        )
                    return Response(
                        status=status.HTTP_201_CREATED,
                        data={
                            "error": True,
                            "message": "Please provide a valid otp if you did not get then resend otp.",
                        },
                    )
                return Response(
                    status=status.HTTP_201_CREATED,
                    data={
                        "error": True,
                        "message": "Please provide a otp if you did not get then resend otp.",
                    },
                )
            else:
                pass


class UserChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserChangePasswordSerializer(
            data=request.data, context={"user": request.user}
        )
        if serializer.is_valid():
            return Response(
                {"message": "Password changed successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"errors": serializer.errors},
            )
        
class UserProfileAPIView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
         queryset = super(UserProfileAPIView, self).get_queryset()
         return queryset
    
class UserResetPasswordEmailLinkAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SendPasswordResetLinkEmailSerializer(data=request.data)
        if serializer.is_valid():
            return Response(
                {
                    "data": serializer.data,
                    "message": "Reset password link sent to the email address",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"errors": serializer.errors},
            )
        
class UserResetPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uid, token):
        serializer = ResetPasswordSerializer(
            data=request.data, context={"uid": uid, "token": token}
        )
        if serializer.is_valid():
            return Response(
                {"message": "Password reset successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"errors": serializer.errors},
                status=status.HTTP_200_OK,
            )