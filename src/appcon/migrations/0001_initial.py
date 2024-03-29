# Generated by Django 3.2.18 on 2023-03-27 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('first_app', '0034_alter_medicament_nbr_unite'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceConsultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.CharField(max_length=50)),
                ('assurance', models.BooleanField(default=False)),
                ('prix', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('consultation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='frais_consultation', to='first_app.consultation')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
