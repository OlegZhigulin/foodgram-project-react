from rest_framework.authtoken.models import TokenProxy


class RusToken(TokenProxy):
    class Meta:
        proxy = True
        verbose_name = 'Токен'
        verbose_name_plural = 'Токены'
