from django.db import models


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
