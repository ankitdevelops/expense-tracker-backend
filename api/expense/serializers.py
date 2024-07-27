from rest_framework import serializers
from api.expense.models import Category, Expense


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CategoryInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, allow_blank=False)
    icon = serializers.ImageField(allow_empty_file=True, required=False)


class ExpenseInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, allow_blank=True)
    amount = serializers.CharField(max_length=20)
    receipt = serializers.ImageField(allow_empty_file=True, required=False)
    category = CategorySerializer(read_only=True)

    def validate_amount(self, value):
        if int(value) <= 0:
            raise serializers.ValidationError("Amount must be positive number")
        return value


class ExpenseOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = "__all__"
