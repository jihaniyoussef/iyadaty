# Generated by Django 3.2.14 on 2022-08-03 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0009_bilantest'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='cnie',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='patient',
            name='mutuelle',
            field=models.CharField(blank=True, choices=[('far', 'FAR'), ('cnops', 'CNOPS'), ('cnss', 'CNSS'), ('assurences', 'ASSURENCES')], max_length=20),
        ),
    ]
