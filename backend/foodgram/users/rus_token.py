from rest_framework.authtoken.models import TokenProxy


class RusToken(TokenProxy):
    class Meta:
        proxy = True
        verbose_name = 'ТОКЕН'
        verbose_name_plural = 'ТОКЕНЫ'
