from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint


class User(AbstractUser):
    USER = "user"
    ADMIN = "admin"
    GUEST = "guest"

    ROLE_CHOICES = [
        (USER, USER),
        (ADMIN, ADMIN),
        (GUEST, GUEST),
    ]

    email = models.EmailField("email", max_length=254, blank=False, unique=True)
    first_name = models.CharField("Имя", max_length=150, blank=False)
    last_name = models.CharField("Фамилия", max_length=150, blank=False)
    password = models.CharField(
        "Пароль",
        max_length=150,
    )

    role = models.CharField(
        "Роль пользователя",
        max_length=50,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
    ]

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_guest(self):
        return self.role == self.GUEST

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Подписчик",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Автор, на которого подписываются",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            UniqueConstraint(fields=["user", "author"], name="unique_follow")
        ]
