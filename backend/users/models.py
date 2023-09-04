from django.db import models
from django.contrib.auth.models import AbstractUser

from foodgram.validators import validate_username


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name="Адрес электронной почты",
        help_text="Адрес электронной почты",
    )

    username = models.CharField(
        unique=True,
        max_length=150,
        validators=(validate_username,),
        verbose_name="Уникальный юзернейм",
        help_text="Уникальный юзернейм",
    )

    first_name = models.CharField(
        max_length=150, blank=True, verbose_name="Имя", help_text="Имя"
    )

    last_name = models.CharField(
        max_length=150, blank=True, verbose_name="Фамилия", help_text="Фамилия"
    )

    password = models.CharField(
        max_length=150, blank=True, verbose_name="Пароль", help_text="Пароль"
    )

    is_admin = models.BooleanField(verbose_name="администратор", default=False)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        constraints = (
            models.UniqueConstraint(
                fields=("username", "email"),
                name="unique_together",
            ),
        )

    def __str__(self):
        return self.username[:20]


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subscriber",
        verbose_name="подписчик",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="author",
        verbose_name="Автор",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ("id",)
        constraints = (
            models.UniqueConstraint(
                fields=(
                    "author",
                    "subscriber",
                ),
                name="unique_subscription",
            ),
        )

    def __str__(self):
        return f"{self.subscriber} подписан на: {self.author}"
