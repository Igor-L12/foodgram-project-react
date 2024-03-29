# Generated by Django 3.2 on 2023-05-09 13:13

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Ingredient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=200, verbose_name="Наименование ингредиента"
                    ),
                ),
                (
                    "measurement_unit",
                    models.CharField(max_length=100, verbose_name="Единица измерения"),
                ),
            ],
            options={
                "verbose_name": "Ингредиент",
                "verbose_name_plural": "Ингредиенты",
            },
        ),
        migrations.CreateModel(
            name="IngredientInRecipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(
                                1,
                                "Колличество ингредиента в рецептне не должно быть менее 1.",
                            )
                        ],
                        verbose_name="Колличество ингредиента в данном рецепте.",
                    ),
                ),
                (
                    "ingredient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="IngredientsInRecipe",
                        to="recipes.ingredient",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ингридиент в рецепте ",
                "verbose_name_plural": "Ингридиенты в рецепте",
            },
        ),
        migrations.CreateModel(
            name="Recipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=200, verbose_name="Название рецепта"),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to="recipes/images/", verbose_name="Картинка"
                    ),
                ),
                ("text", models.TextField(verbose_name="Описание рецепта")),
                (
                    "cooking_time",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(
                                1, "Время приготовление должно быть не менее минуты"
                            )
                        ],
                        verbose_name="Время приготовления в минутах",
                    ),
                ),
                (
                    "pub_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recipes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "ingredients",
                    models.ManyToManyField(
                        related_name="recipes",
                        through="recipes.IngredientInRecipe",
                        to="recipes.Ingredient",
                    ),
                ),
            ],
            options={
                "verbose_name": "Рецепт",
                "verbose_name_plural": "Рецепты",
                "ordering": ("-pub_date",),
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=200, unique=True, verbose_name="Тэг"),
                ),
                ("slug", models.SlugField(unique=True)),
                (
                    "color",
                    models.CharField(
                        max_length=7,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Введите значение цвета в формате HEX! Пример:#FF0000",
                                regex="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
                            )
                        ],
                        verbose_name="Цвет тэга в HEX формате",
                    ),
                ),
            ],
            options={
                "verbose_name": "Тэг",
                "verbose_name_plural": "Тэги",
            },
        ),
        migrations.CreateModel(
            name="ShoppingCart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shopping_cart",
                        to="recipes.recipe",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="RecipeInShoppingList",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Рецепт в списке покупок",
                "verbose_name_plural": "Рецепты в списке покупок",
            },
        ),
        migrations.AddField(
            model_name="recipe",
            name="tags",
            field=models.ManyToManyField(related_name="recipes", to="recipes.Tag"),
        ),
        migrations.AddField(
            model_name="ingredientinrecipe",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="IngredientsInRecipe",
                to="recipes.recipe",
            ),
        ),
        migrations.CreateModel(
            name="Favorite",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="FavoriteRecipe",
                        to="recipes.recipe",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="FavoriteRecipe",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Избранный рецепт",
                "verbose_name_plural": "Избранные рецепты",
            },
        ),
        migrations.AddConstraint(
            model_name="shoppingcart",
            constraint=models.UniqueConstraint(
                fields=("user", "recipe"), name="unique_shopping_cart"
            ),
        ),
        migrations.AddConstraint(
            model_name="favorite",
            constraint=models.UniqueConstraint(
                fields=("user", "recipe"), name="unique_favorite"
            ),
        ),
    ]
