from django.contrib.auth import update_session_auth_hash
from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.serializers import SetPasswordSerializer
from recipes.models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                            ShoppingCart, Tag)
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import Follow, User

from .action import post_and_delete_action
from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPagination
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeGetSerializer, RecipePostSerializer,
                          RecipeShortSerializer, ShoppingCartSerializer,
                          SubscriptionSerializer, TagSerializer,
                          UserGetSerializer, UserPostSerializer,
                          UserWithRecipesSerializer)


class CustomUserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Управление пользователями и подписками.
    Эндпоинты:
    /api/users/
    GET запрос: получить список всех зарегистрированных пользователей
    Подключена пагинация.
    POST запрос: создать нового пользователя. Доступно всем.

    /api/users/{id}
    GET запрос: профиля пользователя. Доступно только авторизованным.

    /api/users/me
    GET запрос: профиль текущего пользователя. Доступно только авторизованным.

    /api/users/set_password/
    POST запрос: смена пароля. Доступно только авторизованным.

    /api/users/subscriptions/
    GET запрос: Возвращает пользователей, на которых
    подписан текущий пользователь.
    Только авторизованным. В выдачу подключены рецепты с возможностью
    установить лимит на их колличество.

    /api/users/{id}/subscribe/
    POST запрос: подписаться на пользователя. Только авторизованным.
    DELETE запрос: отписаться от пользователя.
    """

    queryset = User.objects.all()
    pagination_class = CustomPagination

    def get_instance(self):
        return self.request.user

    def get_serializer_class(self):
        if self.action in ["subscriptions", "subscribe"]:
            return UserWithRecipesSerializer

        elif self.request.method == "GET":
            return UserGetSerializer

        elif self.request.method == "POST":
            return UserPostSerializer

    def get_permissions(self):
        if self.action == "retrieve":
            self.permission_classes = [
                IsAuthenticated,
            ]

        return super(self.__class__, self).get_permissions()

    @action(
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance

        return self.retrieve(request, *args, **kwargs)

    @action(["POST"], detail=False, permission_classes=[IsAuthenticated])
    def set_password(self, request, *args, **kwargs):
        serializer = SetPasswordSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()

        update_session_auth_hash(self.request, self.request.user)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        users = (
            User.objects.filter(following__user=request.user)
            .prefetch_related("recipes")
        )
        page = self.paginate_queryset(users)

        if page is not None:
            serializer = UserWithRecipesSerializer(
                page, many=True, context={"request": request}
            )

            return self.get_paginated_response(serializer.data)

        serializer = UserWithRecipesSerializer(
            users, many=True, context={"request": request}
        )

        return Response(serializer.data)

    @action(
        ["POST", "DELETE"],
        detail=True,
        permission_classes=[IsAuthorOrAdminOrReadOnly],
    )
    def subscribe(self, request, **kwargs):
        return post_and_delete_action(
            self, request, User, Follow, SubscriptionSerializer, **kwargs
        )


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Эндпоинт  api/ingredients/.
    GET запрос: Получение списка всех ингредиентов с
    возможностью поиска по name.
    Эндпоинт  api/ingredients/id.
    GET запрос: получение ингредиента по id
    Права доступа: Доступно без токена.
    """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Эндпоинт  api/tags/.
    GET запрос: Получение списка всех тэгов
    Эндпоинт  api/tags/id.
    GET запрос: получение тэгов по id
    Права доступа: Доступно без токена.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Эндпоинт  api/recipes/.
    GET запрос: Получение списка всех рецептов.
    Страница доступна всем пользователям. Пагинация.
    Доступна фильтрация по избранному, автору, списку покупок и тегам.

    POST запрос: Создать рецепт. Доступно только авторизованному пользователю.

    Эндпоинт  api/recipes/id.
    GET запрос: получение рецепта по id. Доступно только авторизованным.
    PATCH и DELETE запрос доступно только автору рецепта.

    Эндпоинт  api/recipes/favorite.
    POST и DEL запрос: создание и удаление подписки.
    Доступно только авторизованному.

    Эндпоинт api/recipes/download_shopping_cart
    GET запрос: скачать список покупок.
    """

    queryset = Recipe.objects.all()
    permission_classes = [
        IsAuthorOrAdminOrReadOnly,
    ]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RecipeGetSerializer
        elif self.action in [
            "favorite",
            "shopping_cart",
        ]:
            return RecipeShortSerializer

        return RecipePostSerializer

    @action(["POST", "DELETE"], detail=True)
    def favorite(self, request, **kwargs):
        return post_and_delete_action(
            self, request, Recipe, Favorite, FavoriteSerializer, **kwargs
        )

    @action(["POST", "DELETE"], detail=True)
    def shopping_cart(self, request, **kwargs):
        return post_and_delete_action(
            self, request, Recipe, ShoppingCart,
            ShoppingCartSerializer, **kwargs
        )

    @staticmethod
    def send_message(ingredients):
        shopping_list = "Список покупок:"
        for ingredient in ingredients:
            shopping_list += (
                f"\n{ingredient['ingredient__name']} "
                f"({ingredient['ingredient__measurement_unit']}) - "
                f"{ingredient['amount']}"
            )
        filename = "shopping_list.txt"
        response = HttpResponse(shopping_list, content_type="text/plain")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    @action(detail=False, methods=["GET"])
    def download_shopping_cart(self, request):
        ingredients = (
            IngredientInRecipe.objects.filter(
                recipe__shopping_list__user=request.user
            )
            .order_by("ingredient__name")
            .values("ingredient__name", "ingredient__measurement_unit")
            .annotate(amount=Sum("amount"))
        )
        return self.send_message(ingredients)
