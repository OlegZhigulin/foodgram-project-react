from django.contrib import admin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from api.models import Cart, Favorite
from users.models import CustomUser, Subscribe
from users.rus_token import RusToken

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

class RusTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')


admin.site.unregister(Group)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
admin.site.unregister(TokenProxy)
admin.site.register(RusToken, RusTokenAdmin)