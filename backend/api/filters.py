from django_filters import rest_framework

from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart


class IngredientFilter(rest_framework.FilterSet):
    """Фильтр для ингредиентов."""
    name = rest_framework.CharFilter(lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(rest_framework.FilterSet):
    """Фильтр для рецептов: по избранному, списку покупок, автору и тегам."""
    is_favorited = rest_framework.BooleanFilter(
        method='filter_is_favorited__in'
    )
    is_in_shopping_cart = rest_framework.BooleanFilter(
        method='is_in_shopping_cart_method'
    )
    author = rest_framework.NumberFilter(
        field_name='author',
        lookup_expr='exact'
    )
    tags = rest_framework.AllValuesMultipleFilter(
        field_name='tags__slug',
    )

    def filter_is_favorited__in(self, queryset, name, value):
        if value:
            favorites = Favorite.objects.filter(user=self.request.user)
            recipes = [item.recipe.id for item in favorites]
            return queryset.filter(id__in=recipes)
        return queryset


    def is_in_shopping_cart_method(self, queryset, name, value):
        shopping_cart = ShoppingCart.objects.filter(user=self.request.user)
        recipes = [item.recipe.id for item in shopping_cart]
        new_queryset = queryset.filter(id__in=recipes)

        if not value:
            return queryset.difference(new_queryset)

        return queryset.filter(id__in=recipes)

    class Meta:
        model = Recipe
        fields = ('author', 'tags')
