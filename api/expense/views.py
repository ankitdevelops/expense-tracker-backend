from datetime import datetime
from django.utils import timezone
from django.db.models import Q
from django.utils.text import slugify
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError
from .serializers import (
    ExpenseInputSerializer,
    ExpenseOutputSerializer,
    CategorySerializer,
    CategoryInputSerializer,
)
from .models import Category, Expense
from api.utils import APIResponse
from .permissions import IsOwner, IsCategoryOwner


class ExpenseCreateApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = ExpenseInputSerializer(data=request.data)
            if serializer.is_valid():
                category_id = request.data.get("category")
                category = Category.objects.get(id=category_id)
                expense_data = serializer.validated_data
                expense_data["category"] = category
                expense_data["user"] = request.user
                expense = Expense.objects.create(**expense_data)
                res = ExpenseOutputSerializer(expense)
                return APIResponse.success(
                    "record added successfully",
                    data=res.data,
                    status_code=status.HTTP_201_CREATED,
                )
            return APIResponse.error(
                "validation error",
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        except Category.DoesNotExist:
            return APIResponse.error(
                "category not found",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            print(e)
            return APIResponse.error(
                str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )


class ExpenseUpdateApi(APIView):
    permission_classes = [IsOwner, IsAuthenticated]

    def get_object(self, pk):
        try:
            return Expense.objects.get(pk=pk)
        except Expense.DoesNotExist:
            return APIResponse.error(
                "record not found", status_code=status.HTTP_404_NOT_FOUND
            )

    def post(self, request, pk):
        try:
            expense = self.get_object(pk)
            serializer = ExpenseInputSerializer(data=request.data)
            if serializer.is_valid():
                category_id = request.data.get("category")
                category = Category.objects.get(id=category_id)
                expense_data = serializer.validated_data
                expense.amount = expense_data["amount"]
                expense.title = expense_data["title"]
                expense.receipt = expense_data.get("receipt", expense.receipt)
                self.check_object_permissions(request, expense)
                expense.save()

                res = ExpenseOutputSerializer(expense)
                return APIResponse.success(
                    "Record updated successfully",
                    data=res.data,
                    status_code=status.HTTP_200_OK,
                )
            return APIResponse.error(
                "Validation error",
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        except Category.DoesNotExist:
            return APIResponse.error(
                "Category not found",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        except PermissionDenied:
            return APIResponse.error(
                "you don't have permission to perform this action",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        except Exception as e:
            print(e)
            return APIResponse.error(
                str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ExpenseDeleteApi(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request, pk):
        try:
            expense = Expense.objects.get(id=pk)
            self.check_object_permissions(request, expense)

            expense.delete()
            return APIResponse.success(
                "record deleted successfully",
                data={},
                status_code=status.HTTP_200_OK,
            )
        except Expense.DoesNotExist:
            return APIResponse.error(
                "expense not found", status_code=status.HTTP_400_BAD_REQUEST
            )
        except PermissionDenied:
            return APIResponse.error(
                "you don't have permission to perform this action",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        except Exception as e:
            return APIResponse.error(
                str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ExpenseListApi(APIView):

    def calculate_total_expense(self, expenses):
        total_expense_sum = 0
        for expense in expenses:
            total_expense_sum += float(expense.amount)
        return round(total_expense_sum, 2)

    def get(self, request):
        current_date = timezone.now()
        current_month = current_date.month
        current_year = current_date.year
        category_param = request.query_params.get("category")
        start_date_param = request.query_params.get("start_date")
        end_date_param = request.query_params.get("end_date")
        try:
            expenses = Expense.objects.filter(
                user=request.user,
            )

            if start_date_param and end_date_param:
                start_date = timezone.make_aware(
                    datetime.strptime(start_date_param, "%Y-%m-%d")
                )

                end_date = timezone.make_aware(
                    datetime.strptime(end_date_param, "%Y-%m-%d")
                )
                expenses = expenses.filter(
                    created_at__range=(
                        start_date,
                        end_date,
                    )
                )
            elif category_param:
                category = Category.objects.get(id=category_param)
                expenses = expenses.filter(category=category)

            else:
                expenses = expenses.filter(
                    created_at__month=current_month,
                    created_at__year=current_year,
                )

            total_expense_sum = self.calculate_total_expense(expenses=expenses)

            expense_serializer = ExpenseOutputSerializer(expenses, many=True)
            res_data = {
                "expenses": expense_serializer.data,
                "total_expense": total_expense_sum,
            }
            return APIResponse.success(
                "record fetched successfully",
                data=res_data,
                status_code=status.HTTP_200_OK,
            )
        except Expense.DoesNotExist:
            return APIResponse.error(
                "expense not found", status_code=status.HTTP_400_BAD_REQUEST
            )
        except ValidationError as ve:
            error_detail = ve.detail[0] if ve.detail else None
            error_message = (
                str(error_detail) if error_detail else "Validation error occured"
            )
            return APIResponse.error(
                error_message,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        except Category.DoesNotExist:
            return APIResponse.error(
                "category not found", status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return APIResponse.error(
                str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CurrentMonthTotalApi(APIView):

    def calculate_total_expense(self, expenses):
        total_expense_sum = 0
        for expense in expenses:
            total_expense_sum += float(expense.amount)
        return round(total_expense_sum, 2)

    def get(self, request):
        current_date = timezone.now()
        current_month = current_date.month
        current_year = current_date.year
        current_user = request.user

        try:
            expenses = Expense.objects.filter(
                created_at__month=current_month,
                created_at__year=current_year,
                user=current_user,
            )
            total_expense_sum = self.calculate_total_expense(expenses=expenses)
            res_data = {
                "total_expense": total_expense_sum,
            }
            return APIResponse.success(
                "record fetched successfully",
                data=res_data,
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            return APIResponse.error(
                str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CategoryListApi(APIView):

    def get(self, request):
        current_user = request.user
        category_id = request.query_params.get("category_id")
        try:
            categories = Category.objects.filter(
                Q(created_by__role="1") | Q(created_by=current_user)
            )
            if len(categories) < 1:
                return APIResponse.error(
                    "record not found", status_code=status.HTTP_404_NOT_FOUND
                )
            category_serializer = CategorySerializer(categories, many=True)
            return APIResponse.success(
                "record fetched successfully",
                data=category_serializer.data,
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            return APIResponse.error(
                str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CategoryCreateApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = CategoryInputSerializer(data=request.data)
            if serializer.is_valid():
                current_user = request.user
                category_name = request.data.get("title")
                category_name_slug = slugify(category_name)
                category = Category.objects.filter(
                    created_by=current_user, slug=category_name_slug
                )
                if len(category) > 1:
                    return APIResponse.error(
                        "record with this category already exits.",
                        status_code=status.HTTP_400_BAD_REQUEST,
                    )
                validated_category_data = serializer.validated_data
                validated_category_data["created_by"] = current_user
                new_category = Category.objects.create(**validated_category_data)
                res = CategorySerializer(new_category)
                return APIResponse.success(
                    "record created successfully",
                    data=res.data,
                    status_code=status.HTTP_200_OK,
                )
            else:
                return APIResponse.error(
                    "validation error",
                    data=serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            print(e)
            return APIResponse.error(
                str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CategoryUpdateApi(APIView):
    permission_classes = [IsAuthenticated, IsCategoryOwner]

    def post(self, request, pk):
        try:
            category = Category.objects.get(id=pk)
            serializer = CategoryInputSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                title_slug = slugify(validated_data.get("title"))
                category.title = validated_data.get("title")
                category.slug = title_slug
                category.icon = validated_data.get("icon")
                self.check_object_permissions(request, category)
                category.save()
                res = CategorySerializer(category)
                return APIResponse.success(
                    "Record updated successfully",
                    data=res.data,
                    status_code=status.HTTP_200_OK,
                )
            else:
                return APIResponse.error(
                    "validation error",
                    data=serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
        except Category.DoesNotExist:
            return APIResponse.error("record not found", status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return APIResponse.error(
                str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CategoryDeleteApi(APIView):

    permission_classes = [IsAuthenticated, IsCategoryOwner]

    def delete(self, request, pk):
        try:
            category = Category.objects.get(id=pk)
            self.check_object_permissions(request, category)
            category.delete()
            return APIResponse.success(
                "Record deleted successfully",
                status_code=status.HTTP_204_NO_CONTENT,
            )
        except Category.DoesNotExist:
            return APIResponse.error("record not found", status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return APIResponse.error(
                str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
