# Generated by Django 3.2.15 on 2022-08-17 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0022_auto_20220817_0913'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicament',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='medicament',
            name='nbr_unite',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
