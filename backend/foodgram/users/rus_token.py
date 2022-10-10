from rest_framework.authtoken.admin import TokenProxy


class RusTokenProxy(TokenProxy):
    class Meta:
        proxy = True
        verbose_name = 'ТОКЕН'
        verbose_name_plural = 'ТОКЕНЫ'
