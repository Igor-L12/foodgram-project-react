from django.contrib import admin

from .models import Favorite, Ingredient, IngredientInRecipe, Recipe, ShoppingCart, Tag


class RecipeIngredientInline(admin.TabularInline):
    model = IngredientInRecipe
    min_num = 1
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Настройка отображения данных о рецептах."""

    inlines = (RecipeIngredientInline,)
    list_display = (
        "name",
        "author",
        "pub_date",
    )
    list_filter = (
        "name",
        "author",
    )
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Настройки отображения данных о тэгах."""

    list_display = (
        "pk",
        "name",
        "slug",
        "color",
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Настройка отображения данных об ингредиентах."""

    list_display = ("pk", "name", "measurement_unit")


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    """Настройки отображения данных об ингредиентах в рецептах."""

    list_display = ("recipe", "ingredient", "amount")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Настройки отображения данных о рецептах,
    которые пользователи отмечают избранными.
    """

    list_display = ("user", "recipe")


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Настройки отображения списка покупок."""

    list_display = ("user", "recipe")
