from django.contrib import admin

from users.models import CustomUser, Subscribe


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')
    search_fields = ('first_name', 'email')
    list_filter = ('username', 'email')


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
