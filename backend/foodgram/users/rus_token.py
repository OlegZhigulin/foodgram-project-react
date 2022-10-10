from rest_framework.authtoken.models import Token


class RusToken(Token):
    class Meta:
        proxy = True
        verbose_name = 'ТОКЕН'
        verbose_name_plural = 'ТОКЕНЫ'
