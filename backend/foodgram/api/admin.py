from django.contrib import admin
from rest_framework.authtoken.admin import TokenProxy

from api.models import Ingredient, IngredientAmount, Recipe, RusTokenProxy, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)


class IngredientInline(admin.TabularInline):
    model = IngredientAmount
    extra = 10


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'count_favorites')
    search_fields = ('name', 'author')
    list_filter = ('tags', 'author')
    empty_value_display = '-пусто-'
    inlines = (IngredientInline,)

    def count_favorites(self, obj):
        return obj.is_favorited.count()


class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'id')


class RusTokenProxyAdmin(admin.ModelAdmin):
    list_display = ('id',)


admin.site.register(RusTokenProxy, RusTokenProxyAdmin)
admin.site.unregister(TokenProxy)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
