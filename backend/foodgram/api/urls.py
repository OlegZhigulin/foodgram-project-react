from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import IngredientViewSet, RecipeViewSet, TagViewSet

router = SimpleRouter()

router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
