from django.urls import path, include

urlpatterns = [
    path("account/", include("api.account.urls")),
    path("expense/", include("api.expense.urls")),
]
