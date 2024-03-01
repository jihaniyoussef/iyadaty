# Generated by Django 3.2.18 on 2023-03-27 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0034_alter_medicament_nbr_unite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='mutuelle',
            field=models.CharField(blank=True, choices=[('far', 'FAR'), ('cnops', 'CNOPS'), ('cnss', 'CNSS'), ('amo', 'AMO'), ('axa', 'AXA'), ('assurences', 'ASSURENCES')], max_length=20),
        ),
    ]
