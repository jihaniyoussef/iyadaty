# Generated by Django 3.2.18 on 2023-03-28 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0036_auto_20230328_1248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consultation',
            name='pression_arterielle',
        ),
    ]