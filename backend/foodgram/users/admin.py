from django.contrib import admin
from django.contrib.auth.models import Group

from api.models import Cart, Favorite, RusTokenProxy
from users.models import CustomUser, Subscribe


class RusTokenProxyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user')


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')


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
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(RusTokenProxy, RusTokenProxyAdmin)
