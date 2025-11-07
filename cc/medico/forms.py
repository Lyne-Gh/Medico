from django import forms
from .models import Consultation,Traitement, Doctor
from datetime import date

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['patient_nom', 'patient_prenom', 'patient_genre', 'patient_age', 'description']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.date_consultation = date.today() 


class TraitementForm(forms.ModelForm):
    class Meta:
        model = Traitement
        fields = ['medicament', 'quantite', 'contenant', 'duree', 'effects_secondaires']

class DoctorForm(forms.ModelForm):
    SPECIALITY_CHOICES = [
        ('Gynécologue', 'Gynécologue'),
        ('Médecin généraliste', 'Médecin généraliste'),
        ('Cardiologue', 'Cardiologue'),
        ('Pédiatre', 'Pédiatre'),
        ('Dermatologue', 'Dermatologue'),
        ('Ophtalmologue', 'Ophtalmologue'),
        ('Orthopédiste', 'Orthopédiste'),
        ('Neurologue', 'Neurologue'),
        ('Psychiatre', 'Psychiatre'),
        ('Radiologue', 'Radiologue'),
        ('Chirurgien', 'Chirurgien'),
        ('Gastro-entérologue', 'Gastro-entérologue'),
        ('Rhumatologue', 'Rhumatologue'),
        ('Endocrinologue', 'Endocrinologue'),
        ('Urologue', 'Urologue'),
        ('Hématologue', 'Hématologue'),
        ('Infectiologue', 'Infectiologue'),
    ]
    
    first_name = forms.CharField(max_length=100, label='Prénom', widget=forms.TextInput(attrs={'placeholder': 'Prénom du médecin'}))
    last_name = forms.CharField(max_length=100, label='Nom', widget=forms.TextInput(attrs={'placeholder': 'Nom du médecin'}))
    speciality = forms.ChoiceField(choices=SPECIALITY_CHOICES, label='Spécialité', widget=forms.Select())
    
    SHIFT_CHOICES = [
        ('morning', 'Matin (8h - 17h)'),
        ('night', 'Nuit (17h - 8h)'),
    ]
    shift = forms.ChoiceField(choices=SHIFT_CHOICES, label='Type de garde', widget=forms.RadioSelect())
    

    DAYS_OF_WEEK = [
        ('monday', 'Lundi'),
        ('tuesday', 'Mardi'),
        ('wednesday', 'Mercredi'),
        ('thursday', 'Jeudi'),
        ('friday', 'Vendredi'),
        ('saturday', 'Samedi'),
        ('sunday', 'Dimanche'),
    ]
    available_days = forms.MultipleChoiceField(
        choices=DAYS_OF_WEEK,
        label='Jours de travail',
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'speciality', 'shift', 'available_days']
