# Generated by Django 3.2 on 2023-05-13 10:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0010_auto_20230513_1325"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tag",
            name="color",
            field=models.CharField(
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
    ]
