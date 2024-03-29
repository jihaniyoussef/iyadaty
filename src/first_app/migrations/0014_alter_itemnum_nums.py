# Generated by Django 3.2.14 on 2022-08-04 08:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0013_alter_itemnum_nums'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemnum',
            name='nums',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1, "Le nombre d'éléments par page doit être supérieur à 0")]),
        ),
    ]
