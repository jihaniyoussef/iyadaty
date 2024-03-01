# Generated by Django 3.2.14 on 2022-08-11 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0019_testname'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArretTravail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date1', models.DateField()),
                ('date2', models.DateField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('consultation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrettravails', to='first_app.consultation')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]