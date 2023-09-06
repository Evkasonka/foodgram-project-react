from colorfield.fields import ColorField
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import UniqueConstraint
from foodgram.settings import MIN_COOKING_TIME, MIN_INGREDIENTS_AMOUNT
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200, verbose_name="Ингредиент", help_text="Ингредиент"
    )

    measurement_unit = models.CharField(
        max_length=200, verbose_name="Единица измерения",
        help_text="Единица измерения"
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ("name",)

    def __str__(self):
        return self.name[:30]


class Tag(models.Model):
    name = models.CharField(
        max_length=200, unique=True, verbose_name="Тэг", help_text="Тэг"
    )

    color = ColorField(max_length=7, default="#FF0000", unique=True)

    slug = models.SlugField(
        max_length=200,
        unique=True,
        validators=(
            RegexValidator(
                regex=r"^[-a-zA-Z0-9_]+$",
                message=(
                    "Slug должен содержать только "
                    "буквенно-цифровые символы,"
                    "дефисы и символы подчеркивания."
                ),
            ),
        ),
    )

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"
        ordering = ("name",)

    def __str__(self):
        return self.name[:30]


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор",
        help_text="Автор",
    )
    name = models.CharField(
        max_length=200, verbose_name="Название", help_text="Название"
    )

    image = models.ImageField(
        upload_to="recipes/",
        verbose_name="Картинка",
        help_text="Картинка, закодированная в Base64",
    )

    text = models.TextField(verbose_name="Описание",
                            help_text="Описание рецепта")

    ingredients = models.ManyToManyField(
        Ingredient,
        related_name="recipes",
        verbose_name="Ингредиенты",
        help_text="Ингредиенты",
    )

    tags = models.ManyToManyField(
        Tag, related_name="recipes", verbose_name="Тэг", help_text="Тэг"
    )

    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления (в минутах)",
        help_text="Время приготовления (в минутах)",
        validators=(
            MinValueValidator(
                MIN_COOKING_TIME,
                message=f"Минимальное время приготовления = "
                f"{MIN_COOKING_TIME} мин.",
            ),
        ),
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name="дата публикации",
        help_text="дата публикации"
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.text[:30]


class IngredientAmountInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ингредиент",
        help_text="Ингредиент",
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredient_amount_in_recipe",
        verbose_name="Рецепт",
        help_text="Рецепт",
    )

    amount = models.PositiveSmallIntegerField(
        verbose_name="Количество",
        help_text="Количество",
        validators=(
            MinValueValidator(
                MIN_INGREDIENTS_AMOUNT,
                message=f"Минимальное количество ингредиента = "
                f"{MIN_INGREDIENTS_AMOUNT}.",
            ),
        ),
    )

    class Meta:
        verbose_name = "Количество ингредиента в рецепте"
        verbose_name_plural = "Количество ингредиентов в рецептах"
        constraints = (
            UniqueConstraint(
                fields=(
                    "ingredient",
                    "recipe",
                ),
                name="unique_ingredient_recipe",
            ),
        )

    def __str__(self):
        return (
            f"{self.ingredient.name} ({self.ingredient.measurement_unit})"
            f" - {self.amount}"
        )


class IsFavorited(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Пользователь",
        help_text="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Рецепт",
        help_text="Рецепт",
    )

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        constraints = (
            UniqueConstraint(
                fields=(
                    "user",
                    "recipe",
                ),
                name="unique_favorute_recipe",
            ),
        )

    def __str__(self):
        return f'"{self.recipe}" добавлен в избранное {self.user}'


class IsInShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shopping_cart",
        verbose_name="Пользователь",
        help_text="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="shopping_cart",
        verbose_name="Рецепт",
        help_text="Рецепт",
    )

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "списки покупок"
        constraints = (
            UniqueConstraint(
                fields=(
                    "user",
                    "recipe",
                ),
                name="unique_shopping_cart",
            ),
        )

    def __str__(self):
        return f'"{self.recipe}" добавлен в список покупок {self.user}'
