# Generated by Django 3.2.15 on 2022-08-18 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0024_remove_medicament_updated'),
        ('consultation', '0012_pdffacturestore'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsultationDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=500)),
                ('file', models.FileField(upload_to='consultation/documents/%Y/%m/%d/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('consultation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='first_app.consultation')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
