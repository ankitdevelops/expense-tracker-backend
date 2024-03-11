from django.urls import path
from .views import ExpenseCreateApi, ExpenseUpdateApi, ExpenseDeleteApi

urlpatterns = [
    path("add/", ExpenseCreateApi.as_view(), name="add_expense"),
    path("<int:pk>/update/", ExpenseUpdateApi.as_view(), name="update_expense"),
    path("<int:pk>/delete/", ExpenseDeleteApi.as_view(), name="delete_expense"),
]
