# Generated by Django 3.2.14 on 2022-07-29 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0007_auto_20220729_1107'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medicament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('posologie', models.CharField(blank=True, max_length=200)),
                ('nbr_unite', models.CharField(blank=True, max_length=200)),
                ('qsp', models.CharField(blank=True, max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('consultation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medicaments', to='first_app.consultation')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]