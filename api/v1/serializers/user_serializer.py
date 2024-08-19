from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from users.models import Subscription

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""

    class Meta:
        model = User


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки."""

    lesson_count = serializers.SerializerMethodField()
    # TODO сделал

    class Meta:
        model = Subscription
        fields = (
            ['id', 'author', 'title', 'start_date', 'price', 'is_available', 'lesson_count']
            # TODO сделал
        )
