from django.contrib import admin, auth
from django.contrib.auth.models import Group
from rest_framework.authtoken import admin

from api.models import Cart, Favorite
from users.models import RusTokenProxy, Subscribe

User = auth.get_user_model()


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


class RusTokenProxyAdmin(admin.ModelAdmin):
    list_display = ('id', )


admin.site.unregister(Group)
admin.site.unregister(admin.TokenProxy)
admin.site.register(RusTokenProxy, RusTokenProxyAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
