from django import forms
from .models import ServiceConsultation


class  ServiceConsultationForm(forms.ModelForm):
    class Meta:
        model = ServiceConsultation
        fields = ['service', 'assurance', 'prix']
