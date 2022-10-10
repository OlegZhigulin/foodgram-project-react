from rest_framework.authtoken.models import Token


class RusToken(Token):
    class Meta:
        proxy = True
        verbose_name = _("ТОКЕН")
        verbose_name_plural = _("ТОКЕНЫ")
