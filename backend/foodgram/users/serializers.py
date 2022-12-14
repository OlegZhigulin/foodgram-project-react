from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

import api.serializers
from api.models import Recipe
from users.models import CustomUser, Subscribe


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return obj.following.filter(user=user).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class FollowerSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
        read_only_fields = ('email', 'username', 'first_name', 'last_name',)

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj)
        if limit:
            queryset = queryset[:int(limit)]
        return api.serializers.ShortRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return obj.following.filter(user=user).exists()


class FollowCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ('user', 'author')
        read_only_fields = ('user', 'author')

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        subs_id = self.context['request'].parser_context['kwargs']['user_id']
        author = get_object_or_404(CustomUser, id=subs_id)
        user = self.context['request'].user
        if user == author:
            raise serializers.ValidationError(
                '???????????? ?????????????????????? ???? ???????????? ????????'
            )
        if Subscribe.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError(
                f'???? ?????? ?????????????????? ???? ???????????? {author}.'
            )
        return data

    def create(self, validated_data):
        author = get_object_or_404(
            CustomUser,
            id=self.context['request'].parser_context['kwargs']['user_id']
        )
        Subscribe.objects.create(
            user=self.context['request'].user,
            author=author
        )
        return author
