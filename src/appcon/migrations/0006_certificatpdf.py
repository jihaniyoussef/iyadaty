# Generated by Django 3.2.18 on 2023-03-29 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0038_consultation_pression_arterielle'),
        ('appcon', '0005_arretpdf'),
    ]

    operations = [
        migrations.CreateModel(
            name='CertificatPdf',
            fields=[
                ('consultation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='first_app.consultation')),
                ('pdf', models.FileField(upload_to='documents/%Y/%m/%d/')),
            ],
        ),
    ]
