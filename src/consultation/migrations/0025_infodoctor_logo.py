# Generated by Django 3.2.15 on 2022-08-27 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultation', '0024_alter_infodoctor_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='infodoctor',
            name='logo',
            field=models.ImageField(default='logo_doctor.png', upload_to='logo_clinic/'),
        ),
    ]