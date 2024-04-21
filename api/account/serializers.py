from django.core.exceptions import ValidationError
from rest_framework import serializers


class UserRegisterInputSerializer(serializers.Serializer):

    email = serializers.EmailField()
    full_name = serializers.CharField(max_length=255)

    def validate_name(self, value):
        if len(value) < 3:
            raise ValidationError("name is too short.")
        return value


class UserOtpValidateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()

    def validate_otp(self, value):
        if not str(value).isdigit():
            raise ValidationError("otp must only be digits")
        if len(str(value)) < 6:
            raise ValidationError("otp can't be less than 6 digits")
        return value


class RegenerateOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
