from django.shortcuts import get_object_or_404
from recipes.models import Recipe
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import User


@action(detail=True, methods=["post", "delete"])
def post_and_delete_action(
    self, request, recipe_user_model, target_model, serializer, **kwargs
):
    """
    Действия добавления и удаления:
    рецепта в список покупок(recipe_user_model == Recipe, target_model == Shopping_list),
    рецепта в избранное(recipe_user_model == Recipe, target_model == Favorite)
    подписки на пользователей(recipe_user_model == User, target_model == Subscription)
    """
    object_1 = get_object_or_404(recipe_user_model, id=kwargs["pk"])
    data = request.data.copy()
    if recipe_user_model == Recipe:
        data.update({"recipe": object_1.id})
    elif recipe_user_model == User:
        data.update({"author": object_1.id})
    serializer = serializer(data=data, context={"request": request})

    if request.method == "POST":
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            status=status.HTTP_201_CREATED, data=self.get_serializer(object_1).data
        )

    elif request.method == "DELETE" and recipe_user_model == Recipe:
        object = target_model.objects.filter(recipe=object_1, user=request.user)
        if not object.exists():
            return Response(
                {"errors": "В списке покупок(в избранном) нет этого рецепта."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == "DELETE" and recipe_user_model == User:
        object = target_model.objects.filter(author=object_1, user=request.user)
        if not object.exists():
            return Response(
                {"errors": "Вы не подписаны на этого пользователя"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
