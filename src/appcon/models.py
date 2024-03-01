from django.db import models

from first_app.models import Consultation


class ServiceConsultation(models.Model):
    consultation = models.ForeignKey(Consultation,
                                     on_delete=models.CASCADE,
                                     related_name='frais_consultation',)
    service = models.CharField(max_length=50)
    assurance = models.BooleanField(default=False)
    prix = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.service

# models to store pdf for later rendering
class OrdonnacePdf(models.Model):
    consultation = models.OneToOneField(Consultation,
                                        on_delete=models.CASCADE,
                                        primary_key=True,)
    pdf = models.FileField(upload_to='documents/%Y/%m/%d/')


class BilanPdf(models.Model):
    consultation = models.OneToOneField(Consultation,
                                        on_delete=models.CASCADE,
                                        primary_key=True,)
    pdf = models.FileField(upload_to='documents/%Y/%m/%d/')


class FacturePdf(models.Model):
    consultation = models.OneToOneField(Consultation,
                                        on_delete=models.CASCADE,
                                        primary_key=True,)
    pdf = models.FileField(upload_to='documents/%Y/%m/%d/')


class ArretPdf(models.Model):
    consultation = models.OneToOneField(Consultation,
                                        on_delete=models.CASCADE,
                                        primary_key=True,)
    pdf = models.FileField(upload_to='documents/%Y/%m/%d/')


class CertificatPdf(models.Model):
    consultation = models.OneToOneField(Consultation,
                                        on_delete=models.CASCADE,
                                        primary_key=True,)
    pdf = models.FileField(upload_to='documents/%Y/%m/%d/')


class OrientationPdf(models.Model):
    consultation = models.OneToOneField(Consultation,
                                        on_delete=models.CASCADE,
                                        primary_key=True,)
    pdf = models.FileField(upload_to='documents/%Y/%m/%d/')
