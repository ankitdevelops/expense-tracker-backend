from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView


urlpatterns = [path("user/login", TokenObtainPairView.as_view(), name="obtain_token")]
