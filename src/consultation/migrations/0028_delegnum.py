# Generated by Django 3.2.15 on 2022-08-28 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultation', '0027_infodoctor_ville'),
    ]

    operations = [
        migrations.CreateModel(
            name='DelegNum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nums', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
    ]
