from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from api.models import Cart, Recipe
from api.serializers import ShortRecipeSerializer


def shopping_cart_add(self, user, pk):
    if Cart.objects.filter(user=user, recipe__id=pk).exists():
        return Response({
            'errors': 'Рецепт уже добавлен в список'
        }, status=status.HTTP_400_BAD_REQUEST)
    recipe = get_object_or_404(Recipe, id=pk)
    Cart.objects.create(user=user, recipe=recipe)
    serializer = ShortRecipeSerializer(recipe)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def shopping_cart_delete(self, user, pk):
    obj = Cart.objects.filter(user=user, recipe__id=pk)
    if obj.exists():
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({
        'errors': 'Рецепт уже удален'
    }, status=status.HTTP_400_BAD_REQUEST)
