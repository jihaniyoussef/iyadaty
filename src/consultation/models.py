from django.db import models
from tinymce import models as tinymce_models
from tinymce.widgets import TinyMCE
from PIL import Image
from PIL import ImageFile, ImageFilter
import PIL

from first_app.models import Consultation, Patient

ImageFile.LOAD_TRUNCATED_IMAGES = True


class DelegNum(models.Model):
    nums = models.PositiveSmallIntegerField(default=0)


class InfoDoctor(models.Model):
    # french section
    nom = models.CharField(max_length=300, blank=True)
    specialite = models.CharField(max_length=300, blank=True)
    ecole = models.CharField(max_length=300, blank=True)
    # arabic section
    ar_nom = models.CharField(max_length=300, blank=True)
    ar_specialite = models.CharField(max_length=300, blank=True)
    ar_ecole = models.CharField(max_length=300, blank=True)
    gsm = models.CharField(max_length=20, blank=True)
    tel = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=300, blank=True)
    address = models.CharField(max_length=300, blank=True)
    ville = models.CharField(max_length=300, blank=True)
    logo = models.ImageField(upload_to='logo_clinic/',
                             default='logo_doctor.jpg', blank=True)
    logo_center = models.ImageField(upload_to='logo_clinic/',
                             default='logo_doctor.jpg', blank=True)

    def save(self):
        super().save()
        img = Image.open(self.logo.path)
        img1 = Image.open(self.logo.path)
        img = img.convert('RGB')
        img1 = img1.convert('RGB')
        new_img = (70, 70)
        logo_img = (300, 300)
        # logo img
        img.thumbnail(new_img,  PIL.Image.ANTIALIAS)
        img.save(self.logo.path)
        # center img
        img1.thumbnail(logo_img,  PIL.Image.ANTIALIAS)
        # img1 = img1.filter(ImageFilter.GaussianBlur(4))
        img1 = img1.filter(ImageFilter.GaussianBlur(4))
        img1.save(self.logo_center.path)

    def __str__(self):
        return self.nom


class SalleAttente(models.Model):
    MOTIF_CHOICES = (('NC', 'NC'),
                     ('AC', 'AC'),
                     ('CTR', 'CTR'))
    patient = models.ForeignKey(Patient,
                                on_delete=models.CASCADE,
                                related_name='attentes')
    motif = models.CharField(max_length=10, default='NC', choices=MOTIF_CHOICES)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'le patient id: {self.patient.id}'

################### models that go with consultation ############################

class CertificatMedical(models.Model):
    consultation = models.OneToOneField(Consultation,
                                        on_delete=models.CASCADE,
                                        primary_key=True,)
    text = tinymce_models.HTMLField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'certificat de travail pour la consultation {self.consultation.id}'


class LettreOrientation(models.Model):
    consultation = models.OneToOneField(Consultation,
                                        on_delete=models.CASCADE,
                                        primary_key=True,)
    text = tinymce_models.HTMLField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"Lettre d'orientation pour la consultation {self.consultation.id}"


class NomMedicament(models.Model):
    code = models.CharField(max_length=500, blank=True, verbose_name='Code')
    nom = models.CharField(max_length=500, verbose_name='Nom de médicament')
    dci1 = models.CharField(max_length=500, blank=True, verbose_name='DCI1')
    dosage = models.CharField(max_length=200, blank=True, verbose_name='Dosage')
    form = models.CharField(max_length=200, blank=True, verbose_name='Forme')
    presentation = models.CharField(max_length=200, verbose_name='Présentation')
    ppv = models.FloatField(null=True, blank=True, verbose_name='PPV')
    ph = models.FloatField(null=True, blank=True, verbose_name='PH')
    Prix = models.FloatField(null=True, blank=True, verbose_name='Prix brut')
    princeps_generique = models.CharField(
        max_length=100, blank=True, verbose_name='Princeps generique')
    taux_remboursement = models.CharField(
        max_length=100, blank=True, verbose_name='Taux de remboursement')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    updated = models.DateTimeField(auto_now=True)

    @property
    def full_name(self):
        nom = self.nom
        dosage = self.dosage
        if dosage:
            if dosage.lower() in nom.lower():
                return nom
            return f'{nom}, {dosage}'
        else:
            return nom

    class Meta:
        ordering = ('nom',)
        verbose_name = "Médicament"
        verbose_name_plural = "Médicaments"

    def __str__(self):
        return self.nom


class Payment(models.Model):
    consultation = models.ForeignKey(Consultation,
                                     on_delete=models.CASCADE,
                                     related_name='payments')
    description = models.CharField(max_length=500)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def subtotal(self):
        return int(self.price * self.quantity)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.description}: {self.price}'


class PdfStore(models.Model):
    file = models.FileField(upload_to='pdfs/cetificat/')


class PdfLettreStore(models.Model):
    file = models.FileField(upload_to='pdfs/lettre/')


class PdfArretTravailStore(models.Model):
    file = models.FileField(upload_to='pdfs/arret_travail/')


class PdfBilanStore(models.Model):
    file = models.FileField(upload_to='pdfs/bilan/')


class PdfOrdonnanceStore(models.Model):
    file = models.FileField(upload_to='pdfs/ordonnance/')


class PdfFactureStore(models.Model):
    file = models.FileField(upload_to='pdfs/facture/')


class ConsultationDocument(models.Model):
    consultation = models.ForeignKey(Consultation,
                                     on_delete=models.CASCADE,
                                     related_name='documents',)
    name = models.CharField(max_length=100, blank=True)
    file = models.FileField(upload_to='consultation/documents/%Y/')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.description}'


class MotifConsultation(models.Model):
    nom = models.CharField(max_length=200, verbose_name='Motif de consultation')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('nom',)
        verbose_name = "Motif de consultation"
        verbose_name_plural = "Motif de consultation"

    def __str__(self):
        return self.nom


class ExamenClinique(models.Model):
    nom = models.CharField(max_length=200, verbose_name='Examen clinique')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('nom',)
        verbose_name = "Examen clinique"
        verbose_name_plural = "Examens cliniques"

    def __str__(self):
        return self.nom


class Posologie(models.Model):
    nom = models.CharField(max_length=500, verbose_name='Posologie')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('nom',)
        verbose_name = "Posologie"
        verbose_name_plural = "Posologies"

    def __str__(self):
        return self.nom

# quantité
class Quantite(models.Model):
    nom = models.CharField(max_length=500, verbose_name='Quantité')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('nom',)
        verbose_name = "Quantité"
        verbose_name_plural = "Quantités"

    def __str__(self):
        return self.nom
