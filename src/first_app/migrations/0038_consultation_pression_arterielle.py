# Generated by Django 3.2.18 on 2023-03-28 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0037_remove_consultation_pression_arterielle'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultation',
            name='pression_arterielle',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]