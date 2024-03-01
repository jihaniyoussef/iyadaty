from django import forms

from .models import (CertificatMedical, LettreOrientation,
                    Payment, ConsultationDocument, InfoDoctor,
                    DelegNum, SalleAttente)


class SalleAttenteForm(forms.ModelForm):
    class Meta:
        model = SalleAttente
        fields = ['motif',]

class DelegNumForm(forms.ModelForm):
    class Meta:
        model = DelegNum
        fields = ['nums',]

class InfoDoctorForm(forms.ModelForm):
    class Meta:
        model = InfoDoctor
        fields = '__all__'

class CertificatMedicalForm(forms.ModelForm):
    class Meta:
        model = CertificatMedical
        fields = ['text',]


class LettreOrientationForm(forms.ModelForm):
    class Meta:
        model = LettreOrientation
        fields = ['text',]


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['description', 'price', 'quantity']


class ConsultationDocumentForm(forms.ModelForm):
    class Meta:
        model = ConsultationDocument
        fields = ['name', 'file']
