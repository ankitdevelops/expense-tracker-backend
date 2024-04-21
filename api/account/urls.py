from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import UserCreateApi, ValidateOtpApi, RegenerateOtpApi

urlpatterns = [
    path("user/login", TokenObtainPairView.as_view(), name="obtain_token"),
    path("user/register", UserCreateApi.as_view(), name="create_user"),
    path("user/otp/validate", ValidateOtpApi.as_view(), name="validate_otp"),
    path("user/otp/regenerate", RegenerateOtpApi.as_view(), name="regenerate_otp"),
]
