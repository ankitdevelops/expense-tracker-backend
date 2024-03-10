from rest_framework import serializers
from api.expense.models import Category, Expense


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ExpenseInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, allow_blank=True)
    amount = serializers.CharField(max_length=20)
    receipt = serializers.ImageField(allow_empty_file=True)
    category = CategorySerializer(read_only=True)


class ExpenseOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = "__all__"
