from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    REQUIRED_FIELDS = ['username', 'last_name', 'first_name']
    USERNAME_FIELD = 'email'
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=30,
        blank=False
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=False
    )
    email = models.EmailField(blank=False, unique=True)
    USER = 'user'
    ADMIN = 'admin'
    ROLES_CHOICES = (
        (USER, 'User'),
        (ADMIN, 'Admin'),
    )
    role = models.CharField(
        verbose_name='Статус',
        max_length=20,
        choices=ROLES_CHOICES,
        default=USER
    )
    subscriptions = models.ManyToManyField(
        'self', related_name='followers',
        symmetrical=False, through='Subscribe')

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.username)

    @ property
    def is_admin(self):
        return self.role == "admin" or self.is_superuser

    @ property
    def is_user(self):
        return self.role == "user"


class Subscribe(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='follower')
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='following')

    class Meta:
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'user'), name='unique_following'),
        )

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
