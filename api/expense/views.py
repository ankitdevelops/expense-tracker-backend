from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .serializers import ExpenseInputSerializer, ExpenseOutputSerializer
from .models import Category, Expense
from api.utils import APIResponse
from .permissions import IsOwner


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
            raise APIResponse.error(
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
