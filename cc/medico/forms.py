from django import forms
from .models import Consultation
from datetime import date

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['patient_nom', 'patient_prenom', 'patient_genre', 'patient_age', 'description']
    
    # SOOOO THIS IS FOR THE DATE GUYS FYI!! 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.date_consultation = date.today() 
