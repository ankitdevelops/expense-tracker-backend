from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import ExpenseInputSerializer, ExpenseOutputSerializer
from .models import Category, Expense
from api.utils import APIResponse


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
    permission_classes = [IsAuthenticated]

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
            print(request.data)
            if serializer.is_valid():
                category_id = request.data.get("category")
                category = Category.objects.get(id=category_id)
                expense_data = serializer.validated_data
                expense.amount = expense_data["amount"]
                expense.title = expense_data["title"]
                expense.receipt = expense_data["receipt"]
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

        except Exception as e:
            return APIResponse.error(
                str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
