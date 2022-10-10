from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from rest_framework.authtoken.admin import TokenAdmin

User = get_user_model()


class RusTokenProxy(TokenAdmin):
    class Meta:
        proxy = True
        verbose_name = 'ТОКЕН'
        verbose_name_plural = 'ТОКЕНЫ'


class Ingredient(models.Model):
    name = models.TextField(
        verbose_name='Название',
        max_length=200,
        blank=False
    )
    measurement_unit = models.TextField(
        verbose_name='Единица измерения',
        max_length=200,
        blank=False
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = (
            models.UniqueConstraint(
                fields=['measurement_unit', 'name'], name='unique_ingredient'),
        )

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class Tag(models.Model):

    name = models.TextField(
        verbose_name='Название',
        max_length=200,
        blank=False,
        unique=True
    )
    color = models.TextField(
        verbose_name='Цвет',
        max_length=7,
        help_text='В формате НЕХ',
        blank=False
    )
    slug = models.SlugField(
        verbose_name='Уникальный слаг',
        max_length=200,
        validators=[RegexValidator(r'^[\w.@+-]')],
        blank=False
    )

    class Meta:
        ordering = ['id']
        constraints = (
            models.UniqueConstraint(
                fields=['slug', 'name', 'color'], name='unique_tag'),
        )
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    name = models.TextField(
        verbose_name='Название',
        max_length=200,
        blank=False,
    )
    text = models.TextField(
        verbose_name='Описание',
        blank=False,
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления (в минутах)',
        blank=False
    )
    image = models.ImageField(upload_to='recipes/images/',)
    tags = models.ManyToManyField(
        Tag,
        default=None,
        symmetrical=False
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        through_fields=('recipe', 'ingredient'),

        related_name='recipe_of_ingredient'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    is_favorited = models.ManyToManyField(
        User, through='Favorite', through_fields=('recipe', 'user'),)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'name'], name='unique_recipe'),
        )

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='игредиент',
    )
    amount = models.PositiveIntegerField(
        verbose_name='количество',
        help_text='Должно быть целое положительное число',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт',
        related_name='ingredientamounts'
    )

    class Meta:
        verbose_name = 'Количество'
        verbose_name_plural = 'Кол-во ингридиента в рецепте'
        ordering = ['id']
        constraints = (
            models.UniqueConstraint(
                fields=['ingredient', 'amount'], name='unique_ingredients'),
        )

    def __str__(self):
        return f'{self.ingredient} {self.amount}'


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Корзина'
        verbose_name_plural = 'В корзине'
        constraints = [
            models.UniqueConstraint(fields=('user', 'recipe'),
                                    name='unique cart user')
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique favorite recipe for user')
        ]
