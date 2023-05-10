from django.urls import path, include
from rest_framework import routers

from .views import (IngredientViewSet, TagViewSet,
                    RecipeViewSet, CustomUserViewSet)

app_name = 'api'

router = routers.DefaultRouter()

router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
