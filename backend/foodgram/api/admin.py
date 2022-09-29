from django.contrib import admin
from api.models import Ingredient, Tag, Recipe, IngredientAmount


class ingredient_inline(admin.TabularInline):
    model = IngredientAmount
    extra = 10


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'cooking_time', 'count_favorites')
    search_fields = ('name', )
    list_filter = ('tags', 'author')
    empty_value_display = '-пусто-'
    inlines = (ingredient_inline,)

    def count_favorites(self, obj):
        return obj.is_favorite.count()


class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'id')


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
