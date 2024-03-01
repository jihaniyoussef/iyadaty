from django.db import models
from django.conf import settings
from django.urls import reverse
from datetime import date, datetime
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator
from PIL import Image


# Auth models
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, verbose_name='Utilisateur')
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                              blank=True, verbose_name='Photo')

    def save(self):
        super().save()
        img = Image.open(self.photo.path)
        if img.height > 50 or img.width > 50:
            new_img = (50, 50)
            img.thumbnail(new_img)
            img.save(self.photo.path)

    class Meta:
        verbose_name = "Photos d'utilisateurs"
        verbose_name_plural = "Photos d'utilisateurs"

    def __str__(self):
        return f'Profile for user {self.user.username}'


class ItemNum(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='itemnums')
    nums = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, "Le nombre d'éléments par page doit être supérieur à 0"),
        ]
    )


# Clinic Models
PHONE_REGEX = RegexValidator(r'^0\d{9}',
                             "Le numéro de téléphone doit commencer par 0 et avoir une longueur de 10.")


def validate_birth_date(value):
    max_year = date.today().year
    if value > max_year:
        raise ValidationError("La date de naissance ne peut pas être dans le futur!")


class LowerCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(LowerCharField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()


class Patient(models.Model):
    SEXE_CHOICES = (
        ('femme', 'Femme'),
        ('homme', 'Homme'),
    )
    mutuelle_CHOICES = (
        ('far', 'FAR'),
        ('cnops', 'CNOPS'),
        ('cnss', 'CNSS'),
        ('amo', 'AMO'),
        ('axa', 'AXA'),
        ('assurences', 'ASSURENCES'),
    )
    num = models.IntegerField(default=0)
    first_name = LowerCharField(max_length=50)
    last_name = LowerCharField(max_length=50)
    year_of_birth = models.IntegerField(
        validators=[
            validate_birth_date,
            MinValueValidator(1920, "Entrez une date supérier a 1920.")
        ])
    sexe = models.CharField(max_length=10,
                            choices=SEXE_CHOICES, default='homme')
    cnie = models.CharField(max_length=20,
                            blank=True,)
    mutuelle = models.CharField(max_length=20,
                                blank=True,
                                choices=mutuelle_CHOICES)

    phone_number = models.CharField(max_length=30,
                                    blank=True,
                                    validators=[PHONE_REGEX])
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=250, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def age(self):
        today = date.today()
        birth_date = self.year_of_birth
        y = today.year - birth_date
        return y

    @property
    def full_name(self):
        first = self.first_name
        last = self.last_name
        if self.sexe == 'homme':
            name = f'M. {first.capitalize()} {last.capitalize()}'
        else:
            name = f'Mme. {first.capitalize()} {last.capitalize()}'
        return name

    @property
    def name(self):
        first = self.first_name
        last = self.last_name
        if self.sexe == 'homme':
            name = f'M. {first.capitalize()} {last.capitalize()} ({self.age} ans)'
        else:
            name = f'Mme. {first.capitalize()} {last.capitalize()} ({self.age} ans)'
        return name

    class Meta:
        ordering = ('-created',)
        unique_together = ("first_name", "last_name", "year_of_birth", "sexe")

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    # back to it later
    def get_absolute_url(self):
        return reverse('patient_detail', args=[self.id])


class Analyse(models.Model):
    patient = models.ForeignKey(Patient,
                                on_delete=models.CASCADE,
                                related_name='analyses')
    name = models.CharField(max_length=50)
    value = models.FloatField()
    date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return f'{self.name} : {self.value} le {self.date}'


def validate_rdv_date(value):
    if value < date.today():
        raise ValidationError("Un rendez-vous ne peut pas être dans le passe!")


class Appointement(models.Model):
    patient = models.ForeignKey(Patient,
                                on_delete=models.CASCADE,
                                related_name='appointements')
    date = models.DateField(validators=[validate_rdv_date])
    hour = models.TimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def rdv(self):
        return f'Le {self.date.day}/{self.date.month}/{self.date.year} à {self.hour.hour} h {self.hour.minute} min'

    @property
    def date_time(self):
        return datetime(self.date.year, self.date.month,
                        self.date.day, self.hour.hour, self.hour.minute)

    class Meta:
        ordering = ('date', 'hour')

    def __str__(self):
        return f'{self.patient} le {self.date} a {self.hour}'


def validate_poids(value):
    if value < 1:
        raise ValidationError("Entrez un poids positive.")


def validate_taille(value):
    if value < 1:
        raise ValidationError("Entrez une taille positive.")


def validate_temperature(value):
    if value < 1:
        raise ValidationError("Entrez une température positive.")


def validate_frequence(value):
    if value < 1:
        raise ValidationError("Entrez une fréquence cardiaque positive.")


def validate_pression(value):
    if value < 1:
        raise ValidationError("Entrez une préssion artielle positive.")


def validate_imc(value):
    if value < 0:
        raise ValidationError("Entrez une valeur positive.")


def validate_sao2(value):
    if value < 0 or value > 100:
        raise ValidationError("Entrez une valeur entre 0 et 100.")


class Consultation(models.Model):
    patient = models.ForeignKey(Patient,
                                on_delete=models.CASCADE,
                                related_name='consultations')
    motif = models.TextField(blank=True)
    antecedant = models.TextField(blank=True)
    diagnostique = models.TextField(blank=True)
    examen = models.TextField(blank=True)
    poids_kg = models.IntegerField(null=True, blank=True, validators=[validate_poids])
    taille_cm = models.IntegerField(blank=True, null=True, validators=[validate_taille])
    imc = models.FloatField(blank=True, null=True, validators=[validate_imc])
    sao2 = models.IntegerField(blank=True, null=True, validators=[validate_sao2])
    temperature_degC = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, validators=[validate_temperature])
    frequence_cardiaque = models.IntegerField(
        blank=True, null=True, validators=[validate_frequence])
    pression_arterielle = models.CharField(blank=True, max_length=20)
    observation = models.TextField(blank=True)
    ct = models.CharField(blank=True, max_length=50)
    hdl = models.CharField(blank=True, max_length=50)
    ldl = models.CharField(blank=True, max_length=50)
    tg = models.CharField(blank=True, max_length=50)
    g = models.CharField(blank=True, max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.patient.name} - {self.motif}'


class Medicament(models.Model):
    consultation = models.ForeignKey(Consultation,
                                     on_delete=models.CASCADE,
                                     related_name='medicaments')
    name = models.CharField(max_length=500)
    posologie = models.CharField(max_length=500, blank=True)
    nbr_unite = models.CharField(max_length=500, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.name}'


class BilanTest(models.Model):
    consultation = models.ForeignKey(Consultation,
                                     on_delete=models.CASCADE,
                                     related_name='tests')
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.name}'


class TestName(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nom de bilan')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Bilan'
        verbose_name_plural = 'Bilans'

    def __str__(self):
        return f'{self.name}'


class ArretTravail(models.Model):
    consultation = models.OneToOneField(Consultation,
                                        on_delete=models.CASCADE,
                                        primary_key=True,)
    date1 = models.DateField()
    date2 = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'arret de travail du {self.date1} au {self.date2}'

    @property
    def total_days(self):
        delta = self.date2 - self.date1
        return delta.days
