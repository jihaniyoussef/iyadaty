# Generated by Django 3.2.15 on 2022-09-01 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultation', '0034_posologie'),
    ]

    operations = [
        migrations.AddField(
            model_name='infodoctor',
            name='logo_center',
            field=models.ImageField(default='logo_doctor.jpg', upload_to='logo_clinic/'),
        ),
    ]
