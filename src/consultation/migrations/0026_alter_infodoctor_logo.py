# Generated by Django 3.2.15 on 2022-08-27 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultation', '0025_infodoctor_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infodoctor',
            name='logo',
            field=models.ImageField(default='logo_doctor.jpg', upload_to='logo_clinic/'),
        ),
    ]
