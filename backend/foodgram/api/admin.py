from django.contrib import admin

from api.models import Ingredient, Recipe, IngredientAmount


class IngredientInline(admin.TabularInline):
    model = IngredientAmount
    extra = 10


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name')
    search_fields = ('name')


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'count_favorites')
    search_fields = ('name', 'author')
    list_filter = ('tags', 'author')
    empty_value_display = '-пусто-'
    inlines = (IngredientInline,)

    def count_favorites(self, obj):
        return obj.is_favorited.count()


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)

