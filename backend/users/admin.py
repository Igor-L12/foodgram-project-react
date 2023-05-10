from django.contrib import admin

from .models import User, Follow


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """ Возможность редактировать и удалять
    данные о пользователях. Фильтрация по email и username.
    """
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'password',
        'role',
    )
    search_fields = ('username',)
    list_filter = ('username', 'email')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Класс для настройки отображения данных о подписках."""
    list_display = ('user', 'author')
