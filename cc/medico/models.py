from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

# Create your models here.
class Consultation(models.Model):
    GENRE_CHOIX = [('F', "Femme"), ('H', "Homme")]
    patient_nom = models.CharField(max_length=40, null=False)
    patient_prenom = models.CharField(max_length=30, null=False)
    patient_genre = models.CharField(max_length=1, null=False, choices=GENRE_CHOIX)
    patient_age = models.IntegerField(null=False)
    description = models.TextField(null=False)
    date_consultation = models.DateField(null=False)

def __str__(self):
    return self.patient_nom

class Traitement(models.Model):
    medicament=models.CharField(max_length=40, null=False)
    quantite=models.IntegerField(null=False)
    contenant=models.CharField(max_length=20, null=False)
    duree=models.IntegerField(null=False)  # durée en jours
    effects_secondaires=models.TextField(null=False, blank=True)
    consultation=models.ForeignKey(Consultation, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.medicament

class Doctor(models.Model):
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
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=50, choices=SPECIALITY_CHOICES)
    password = models.CharField(max_length=100, default="D000000")
    shift = models.CharField(max_length=10)
    start_time = models.CharField(max_length=5, blank=True)
    end_time = models.CharField(max_length=5, blank=True)
    available_days = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.speciality}"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.password == "D000000":
                self.set_password(self.password)
        super(Doctor, self).save(*args, **kwargs)

class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        if not self.pk or not self.password.startswith('pbkdf2_'):
            self.set_password(self.password)
        super().save(*args, **kwargs)

class Appointment(models.Model):
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"({self.appointment_date} {self.appointment_time})"
