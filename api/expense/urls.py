from django.urls import path
from .views import ExpenseCreateApi, ExpenseUpdateApi

urlpatterns = [
    path("add/", ExpenseCreateApi.as_view(), name="add_expense"),
    path("<int:pk>/update", ExpenseUpdateApi.as_view(), name="update_expense"),
]
