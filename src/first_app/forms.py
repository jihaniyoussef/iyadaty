from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date

from .models import (Patient, ItemNum, Appointement, Consultation,
                     Medicament, BilanTest, Analyse)


# Custom login Form

class CustomLoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login':
            "Veuillez saisir un nom d'utilisateur et un mot de passe corrects.",
        'inactive': "Ce compte est inactif.",
    }


class CustomPasswordChangeForm(PasswordChangeForm):
    error_messages = {
        'password_mismatch': "Les deux champs de mot de passe ne correspondaient pas.",
        'password_notvalid': "Le mot de passe doit comporter 8 caractères contenant des caractères alphanumériques avec au moins 1 caractère spécial et 1 majuscule.",
        'password_incorrect': "Votre ancien mot de passe est incorrect. Veuillez le saisir à nouveau.",
    }


class SearchForm(forms.Form):
    query = forms.CharField()
    id = forms.IntegerField(widget=forms.HiddenInput(),)


class TodayForm(forms.Form):
    today = forms.DateField(initial=date.today())


class ItemNumForm(forms.ModelForm):
    class Meta:
        model = ItemNum
        fields = ['nums', ]

################################# patient forms #############


class AddAnalyseForm(forms.ModelForm):
    class Meta:
        model = Analyse
        fields = ['value', 'date', ]


class AddPatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'year_of_birth',
                  'sexe', 'cnie', 'mutuelle', 'phone_number', 'email', 'address',
                  ]
        error_messages = {

            NON_FIELD_ERRORS: {
                'unique_together': "Vous avez déjà un patient avec le même nom, prénom, âge et sexe.",
            }

        }

    def __init__(self, *args, **kwargs):
        super(AddPatientForm, self).__init__(*args, **kwargs)
        # update errors
        self.fields['first_name'].error_messages = {
            'required': 'Entrez le prénom du patient.',
            'max_length': 'La longueur du prénom ne doit pas dépasser 50 caractères.',
        }
        self.fields['last_name'].error_messages = {
            'required': 'Entrez le nom du patient.',
            'max_length': 'La longueur du prénom ne doit pas dépasser 50 caractères.',
        }
        self.fields['year_of_birth'].error_messages = {
            'required': 'Entrez la date de naissance du patient.',
            'invalid': 'Entrez une date valide.',
        }
        self.fields['email'].error_messages = {
            'invalid': 'Entrez une addresse email valide.',
        }


class AddAppointementForm(forms.ModelForm):
    patient = forms.CharField(max_length=200)
    patient_id = forms.IntegerField(widget=forms.HiddenInput(),)

    class Meta:
        model = Appointement
        fields = ['date', 'hour', ]

    def __init__(self, *args, **kwargs):
        super(AddAppointementForm, self).__init__(*args, **kwargs)
        # update errors
        self.fields['date'].error_messages = {
            'required': 'Entrez la date du rendez-vous.',
            'invalid': 'Entrez une date valide.',
        }
        self.fields['hour'].error_messages = {
            'required': "Entrez l'heure du rendez-vous",
            'invalid': "Entrez une heure valide.",
        }


class EditAppointementForm(forms.ModelForm):
    class Meta:
        model = Appointement
        fields = ['date', 'hour', ]

    def __init__(self, *args, **kwargs):
        super(EditAppointementForm, self).__init__(*args, **kwargs)
        # update errors
        self.fields['date'].error_messages = {
            'required': 'Entrez la date du rendez-vous.',
            'invalid': 'Entrez une date valide.',
        }
        self.fields['hour'].error_messages = {
            'required': "Entrez l'heure du rendez-vous",
            'invalid': "Entrez une heure valide.",
        }

class AddConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['motif', 'diagnostique', 'examen', 'imc', 'sao2',
                  'poids_kg', 'taille_cm', 'temperature_degC', 'antecedant',
                  'frequence_cardiaque', 'pression_arterielle',
                  'observation', 'ct', 'hdl', 'ldl', 'tg', 'g']

    def __init__(self, *args, **kwargs):
        super(AddConsultationForm, self).__init__(*args, **kwargs)
        # update errors
        self.fields['motif'].error_messages = {
            'required': 'Entrez le motif de la consultation.',
            'max_length': 'La longueur du prénom ne doit pas dépasser 500 caractères.',
        }
        self.fields['antecedant'].error_messages = {
            'required': 'Entrez les antécédents.',
            'max_length': 'La longueur du prénom ne doit pas dépasser 500 caractères.',
        }
        self.fields['poids_kg'].error_messages = {
            'invalid': 'Entrez un poids valide.',
        }
        self.fields['taille_cm'].error_messages = {
            'invalid': 'Entrez une taille valide.',
        }
        self.fields['temperature_degC'].error_messages = {
            'invalid': 'Entrez une temperature valide.',
        }
        self.fields['frequence_cardiaque'].error_messages = {
            'invalid': 'Entrez une fréquence cardiaque valide.',
        }
        self.fields['pression_arterielle'].error_messages = {
            'invalid': 'Entrez une pression arterielle valide.',
        }


class AddAppointementConsultationForm(forms.ModelForm):
    class Meta:
        model = Appointement
        fields = ['date', 'hour', ]

    def __init__(self, *args, **kwargs):
        super(AddAppointementConsultationForm, self).__init__(*args, **kwargs)
        # update errors
        self.fields['date'].error_messages = {
            'required': 'Entrez la date du rendez-vous.',
            'invalid': 'Entrez une date valide.',
        }
        self.fields['hour'].error_messages = {
            'required': "Entrez l'heure du rendez-vous",
            'invalid': "Entrez une heure valide.",
        }

# Export excel form


def validate_date(value):
    today = date.today()
    if value > today:
        raise ValidationError('La date ne peut pas être dans le futur!')


class ExportExcelFrom(forms.Form):
    error_messages = {
        'invalid': 'Entrez une date valide.',
    }
    date1 = forms.DateField(validators=[validate_date])
    date2 = forms.DateField(validators=[validate_date])

    def clean_date2(self):
        cd = self.cleaned_data
        if cd['date1'] > cd['date2']:
            raise ValidationError(
                'La date de fin doit être supérieure ou égale à la date de début.')
        return cd['date2']

    def __init__(self, *args, **kwargs):
        super(ExportExcelFrom, self).__init__(*args, **kwargs)
        # update errors
        self.fields['date1'].error_messages = {
            'required': 'Entrez la date de début.',
            'invalid': 'Entrez une date valide.',
        }
        self.fields['date2'].error_messages = {
            'required': "Entrez la date de fin",
            'invalid': "Entrez une heure valide.",
        }


class MedicamentForm(forms.ModelForm):
    class Meta:
        model = Medicament
        fields = ['name', 'posologie', 'nbr_unite', ]


class ArretTravailFrom(forms.Form):
    error_messages = {
        'invalid': 'Entrez une date valide.',
    }
    date1 = forms.DateField()
    date2 = forms.DateField()

    def clean_date2(self):
        cd = self.cleaned_data
        if cd['date1'] > cd['date2']:
            raise ValidationError(
                'La date de fin doit être supérieure ou égale à la date de début.')
        return cd['date2']

    def __init__(self, *args, **kwargs):
        super(ArretTravailFrom, self).__init__(*args, **kwargs)
        # update errors
        self.fields['date1'].error_messages = {
            'required': 'Entrez la date de début.',
            'invalid': 'Entrez une date valide.',
        }
        self.fields['date2'].error_messages = {
            'required': "Entrez la date de fin",
            'invalid': "Entrez une date valide.",
        }
