# Generated by Django 3.2.15 on 2022-08-27 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultation', '0023_infodoctor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infodoctor',
            name='address',
            field=models.CharField(max_length=300),
        ),
    ]