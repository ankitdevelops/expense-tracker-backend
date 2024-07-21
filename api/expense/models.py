from django.db import models
from django.conf import settings


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=500)
    icon = models.ImageField(upload_to="category/icon/", blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class Expense(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    amount = models.CharField(max_length=20)
    receipt = models.ImageField(
        upload_to="receipt/%Y/%m/",
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user.full_name} spent RS: {self.amount}"
