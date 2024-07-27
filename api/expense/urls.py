from django.urls import path
from .views import (
    ExpenseCreateApi,
    ExpenseUpdateApi,
    ExpenseDeleteApi,
    ExpenseListApi,
    CurrentMonthTotalApi,
    CategoryListApi,
    CategoryCreateApi,
    CategoryUpdateApi,
    CategoryDeleteApi,
)

urlpatterns = [
    path("add/", ExpenseCreateApi.as_view(), name="add_expense"),
    path("list/", ExpenseListApi.as_view(), name="list_api"),
    path(
        "current/",
        CurrentMonthTotalApi.as_view(),
        name="current_month_total",
    ),
    path(
        "<int:pk>/update/",
        ExpenseUpdateApi.as_view(),
        name="update_expense",
    ),
    path(
        "<int:pk>/delete/",
        ExpenseDeleteApi.as_view(),
        name="delete_expense",
    ),
    path("category/list", CategoryListApi.as_view(), name="category-list"),
    path("category/create", CategoryCreateApi.as_view(), name="category-create"),
    path(
        "category/update/<int:pk>", CategoryUpdateApi.as_view(), name="category-update"
    ),
    path(
        "category/delete/<int:pk>", CategoryDeleteApi.as_view(), name="category-delete"
    ),
]
