from rest_framework import serializers
from .models import Ad, Category, Condition
from django.contrib.auth import get_user_model

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ['id', 'name']


class AdSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    category_name = serializers.CharField(write_only=True, required=False)
    condition_name = serializers.CharField(write_only=True, required=False)
    category = CategorySerializer(read_only=True)
    condition = ConditionSerializer(read_only=True)

    class Meta:
        model = Ad
        fields = [
            'id',
            'user',
            'created_at',
            'title',
            'description',
            'category',
            'condition',
            'category_name',
            'condition_name'
        ]

    def validate(self, data):
        category_name = data.pop('category_name', None)
        condition_name = data.pop('condition_name', None)

        if category_name:
            try:
                data['category'] = Category.objects.get(name=category_name)
            except Category.DoesNotExist:
                raise serializers.ValidationError({'category': 'Invalid category name'})

        if condition_name:
            try:
                data['condition'] = Condition.objects.get(name=condition_name)
            except Condition.DoesNotExist:
                raise serializers.ValidationError({'condition': 'Invalid condition name'})

        return data