import base64

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.db import transaction
from rest_framework import serializers

from users.serializers import CustomUserSerializer
from api.models import Favorite, Ingredient, IngredientAmount, Recipe, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    amount = serializers.IntegerField(
        max_value=2147483647,
        min_value=0,
        error_messages={
            'Ошибка': 'Введите число в диапазане от 0 до 2147483647'},
    )

    class Meta:
        model = IngredientAmount
        fields = ['id', 'name', 'amount', 'measurement_unit', ]


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('user', 'recipe')
        model = Favorite


class ShortRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(allow_null=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientAmountSerializer(
        source='ingredientamounts', many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'author', 'name', 'text', 'cooking_time', 'tags',
            'ingredients', 'image', 'is_favorited', 'is_in_shopping_cart'
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(favorites__user=user, id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(cart__user=user, id=obj.id).exists()

    def validate_ingredients(self, data):
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError({
                'ingredients': 'Без ингредиентов не будет рецепта'})
        ingredient_list = []
        for ingredient_item in ingredients:
            try:
                ingredient = Ingredient.objects.get(pk=ingredient_item['id'])
            except ObjectDoesNotExist:
                raise serializers.ValidationError('Такого ингредиента нет')
            if ingredient_item in ingredient_list:
                raise serializers.ValidationError('Повторение ингредиентов')
            if int(ingredient_item['amount']) < 0:
                raise serializers.ValidationError({
                    'ingredients': ('Количество больше нуля')
                })
            if int(ingredient_item['amount']) > 2147483647:
                raise serializers.ValidationError({
                    'ingredients': ('Слишком большое число')
                })
            ingredient_list.append(ingredient)
        return data

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            IngredientAmount.objects.get_or_create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )

    def update_ingredients(self, ingredients_data, recipe):
        id_data = [ingredient.get('id') for ingredient in ingredients_data]
        recipe_ingredients = [
            ingredients.id for ingredients in recipe.ingredients.all()]
        for new_ingredient in ingredients_data:
            new_ingredient_id = new_ingredient.get('id')
            print(new_ingredient.get('amount'))
            if new_ingredient_id not in recipe_ingredients:
                IngredientAmount.objects.create(
                    recipe=recipe,
                    ingredient_id=new_ingredient_id,
                    amount=new_ingredient.get(
                        'amount'),
                )
            else:
                IngredientAmount.objects.filter(
                    recipe=recipe,
                    ingredient_id=new_ingredient_id
                ).update(
                    amount=new_ingredient.get('amount'))

        for ingredient_id in recipe_ingredients:
            if ingredient_id not in id_data:
                IngredientAmount.objects.filter(
                    recipe=recipe, ingredient_id=ingredient_id).delete()

    @transaction.atomic
    def create(self, validated_data):
        image = validated_data.pop('image')
        ingredients_data = self.initial_data.get('ingredients')
        recipe = Recipe.objects.create(image=image, **validated_data)
        tags_data = self.initial_data.get('tags')
        recipe.tags.set(tags_data)
        self.create_ingredients(ingredients_data, recipe)
        recipe.save()
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        tags_data = self.initial_data.get('tags')
        instance.tags.set(tags_data)
        ingredients_data = self.initial_data.get('ingredients')
        self.update_ingredients(ingredients_data, instance)
        instance.save()
        return instance
