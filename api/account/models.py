from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class MyAccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("User Must have a unique phone_number")

        user = self.model(
            email=email,
        )
        user.is_active = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    # function to create superuser

    def create_superuser(self, email, password):
        user = self.create_user(
            email=email,
            password=password,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("0", "User"),
        ("1", "Staff"),
    )
    full_name = models.CharField(max_length=255)
    email = models.EmailField(
        max_length=300,
        unique=True,
    )
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default="0")
    otp = models.CharField(max_length=6, null=True)
    otp_created_time = models.DateTimeField(null=True)

    USERNAME_FIELD = "email"
    objects = MyAccountManager()

    def __str__(self):
        return f"{self.full_name}"
