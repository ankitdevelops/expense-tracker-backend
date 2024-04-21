from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    UserRegisterInputSerializer,
    UserOtpValidateSerializer,
    RegenerateOtpSerializer,
)
from .models import User
from api.utils import send_email, APIResponse


class UserCreateApi(APIView):
    def post(self, request):
        try:
            serializer = UserRegisterInputSerializer(data=request.data)
            if serializer.is_valid():
                user_email = request.data.get("email")
                check_user = User.objects.filter(email=user_email).exists()
                if check_user:
                    return APIResponse.error(
                        "user already exists with this email",
                        data={},
                        status_code=status.HTTP_400_BAD_REQUEST,
                    )
                user = User.objects.create(**serializer.validated_data)
                user.generate_otp()
                user.save()
                otp = user.otp
                print(user)
                email_status = send_email(
                    "Otp",
                    f"Please dont share your otp with any other \n \n {otp}",
                    [user.email],
                )
                if email_status:
                    return APIResponse.success(
                        "user created successfully",
                        data={},
                        status_code=status.HTTP_201_CREATED,
                    )
                else:
                    return APIResponse.error(
                        "error while sending otp",
                        data={},
                        status_code=status.HTTP_400_BAD_REQUEST,
                    )
            return APIResponse.error(
                "validation error",
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            print(e)
            return APIResponse.error(
                "Failed to register user",
                status_code=status.HTTP_400_BAD_REQUEST,
            )


class ValidateOtpApi(APIView):
    def post(self, request):
        try:
            serializer = UserOtpValidateSerializer(data=request.data)
            if serializer.is_valid():
                otp = serializer.validated_data["otp"]
                email = serializer.validated_data["email"]
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    return APIResponse.error(
                        "user not found",
                        data={},
                        status_code=status.HTTP_400_BAD_REQUEST,
                    )
                if user.otp is None:
                    return APIResponse.error(
                        "Invalid OTP1",
                        data={},
                        status_code=status.HTTP_400_BAD_REQUEST,
                    )
                if str(otp) != str(user.otp):
                    return APIResponse.error(
                        "Invalid OTP2",
                        data={},
                        status_code=status.HTTP_400_BAD_REQUEST,
                    )
                otp_created_time = user.otp_created_time
                current_time = timezone.now()
                if (current_time - otp_created_time) > timedelta(minutes=5):
                    return APIResponse.error(
                        "otp has been expired",
                        data={},
                        status_code=status.HTTP_400_BAD_REQUEST,
                    )
                user.is_active = True
                user.save()
                refresh_token = RefreshToken.for_user(user)
                access_token = str(refresh_token.access_token)

                return APIResponse.success(
                    "otp validated successfully",
                    data={
                        "access_token": access_token,
                        "refresh_token": str(refresh_token),
                    },
                    status_code=status.HTTP_201_CREATED,
                )
            else:
                return APIResponse.error(
                    "validation error",
                    data=serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            print(e)
            return APIResponse.error(
                "Failed to validate the otp, please try again after sometime",
                status_code=status.HTTP_400_BAD_REQUEST,
            )


class RegenerateOtpApi(APIView):
    def post(self, request):
        try:
            serializer = RegenerateOtpSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data["email"]
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    return APIResponse.error(
                        "user not found",
                        data={},
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                user.generate_otp()
                user.save()
                email_status = send_email(
                    "Otp",
                    f"Please dont share your otp with any other \n \n  \n{user.otp}",
                    [user.email],
                )
                if email_status:
                    return APIResponse.success(
                        "otp sent successfully",
                        data={},
                        status_code=status.HTTP_201_CREATED,
                    )
                else:
                    return APIResponse.error(
                        "error while sending otp",
                        status_code=status.HTTP_400_BAD_REQUEST,
                    )

        except Exception as e:
            print(e)
            return APIResponse.error(
                "Failed to validate the otp, please try again after sometime",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
