# Generated by Django 3.2 on 2023-05-12 20:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("recipes", "0006_auto_20230512_2322"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="favorite",
            name="unique_favorite_recipe_shopping_cart",
        ),
        migrations.AlterField(
            model_name="favorite",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="FavoriteRecipe",
                to="recipes.recipe",
            ),
        ),
        migrations.AlterField(
            model_name="favorite",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="FavoriteRecipe",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="shoppingcart",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="shopping_cart",
                to="recipes.recipe",
            ),
        ),
        migrations.AlterField(
            model_name="shoppingcart",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="RecipeInShoppingList",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddConstraint(
            model_name="favorite",
            constraint=models.UniqueConstraint(
                fields=("user", "recipe"), name="unique_favorite"
            ),
        ),
    ]
