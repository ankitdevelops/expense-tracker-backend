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


class SetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=10, max_length=20, allow_blank=False, trim_whitespace=True
    )
    confirm_password = serializers.CharField(
        min_length=10, max_length=20, allow_blank=False, trim_whitespace=True
    )

    def validate(self, data):
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")

        return data
