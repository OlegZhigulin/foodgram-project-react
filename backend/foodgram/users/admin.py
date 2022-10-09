from django.contrib import admin, auth
from django.contrib.auth.models import Group

from api.models import Cart, Favorite

User = auth.get_user_model()


class CartInline(admin.TabularInline):
    model = Cart
    extra = 10


class FavoriteInline(admin.TabularInline):
    model = Favorite
    extra = 10


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')
    search_fields = ('first_name', 'email')
    list_filter = ('username', 'email')
    inlines = (CartInline, FavoriteInline)


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
