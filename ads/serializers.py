from rest_framework import serializers
from .models import Ad, Category, Condition, ExchangeProposal
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


class ExchangeSerializer(serializers.ModelSerializer):
    ad_sender = AdSerializer(read_only=True)
    ad_receiver = AdSerializer(read_only=True)
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = ExchangeProposal
        fields = [
            'id',
            'ad_sender',
            'ad_receiver',
            'status',
            'status_display',
            'comment'
        ]
        read_only_fields = ['id', 'ad_sender', 'ad_receiver']

    def get_status_display(self, obj):
        return obj.get_status_display()
