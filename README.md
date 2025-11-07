#CC1 framwork web

#Membres du groupe
Del Carmen Villilo Margerit margerit.del-carmen-villilo@etu.univ-orleans.fr
Langlois Clément L3 Miage - clement.langlois1@etu.univ-orleans.fr
Bitodi Christian - christian.bitodi@etu.univ-orleans.fr
GHRIBI Lyne L3 ING - Université d'Orléans  lyne.ghribi@etu.univ-orleans.fr
#commandes faites
#pour cree le projet 
django-admin start project cc 
#pour deplacer le fichier manage.py
mv cc/manage.py .
#pour cree l'appli medico
python manage.py startapp medico

#Question 4 : - Bitodi Christian :
 - mkdir medico/fixtures (Créer le dossier fixtures qui contiendra examples.json)
 - python cc/manage.py dumpdata medico --indent 4 > cc/medico/fixtures/examples.json (Extraire les données dans la base 
 [--ident 4 sert à indenter les champs pour les  reconnaitre plus facilement])
 -  cd cc && python manage.py loaddata examples (Charger les données du fichier examples.json dans la base)

#question 5

python manage.py shell
from medico.models import Consultation
from datetime import date


Consultation.objects.create(
    patient_nom="Dupont",
    patient_prenom="Alice",
    patient_genre="F",
    patient_age=34,
    description="Douleurs dorsales depuis 2 semaines.",
    date_consultation=date(2025, 10, 10)
)


Consultation.objects.create(
    patient_nom="Martin",
    patient_prenom="Paul",
    patient_genre="H",
    patient_age=45,
    description="Toux persistante depuis 3 semaines, légère fièvre.",
    date_consultation=date(2025, 9, 30)
)


Consultation.objects.create(
    patient_nom="Durand",
    patient_prenom="Claire",
    patient_genre="F",
    patient_age=28,
    description="Migraine récurrente et fatigue importante.",
    date_consultation=date(2025, 10, 5)
)

exit()

#Question 10 : - Bitodi Christian :
 - pip install django-bootstrap5 (installer BootStrap5 et l'ajouter dans settings.py)
 - cela a servi à  utiliser des balises de template  comme : 
{% load django_bootstrap5 %}
{% block content %}
{% endblock %}



#question11 -> creation des traitements sur shell
from app_name.models import Consultation, Traitement
c2 = Consultation.objects.get(id=2)
c3 = Consultation.objects.get(id=3)
t1 = Traitement.objects.create(
    medicament="Paracétamol",
    quantite=2,
    contenant="comprimé",
    duree=5,
    effects_secondaires="Somnolence légère",
    consultation=c2
)

t2 = Traitement.objects.create(
    medicament="Amoxicilline",
    quantite=3,
    contenant="gélule",
    duree=7,
    effects_secondaires="Nausées possibles",
    consultation=c3
)




#Question12
Il y a 2 façons d'ajouter un traitement, dans la liste des consultations avec le bouton 
[+]Traitement ou dans les détails d'une consultation avec le bouton ajouter consultation

#Question 12 -(Partie - Suprimer Traitement) : - Bitodi Christian :
Il y a 3 manières de supprimer un traitement : (1) : dans la liste des consultations avec le bouton 
[-]Traitement | (2) : dans les détails d'une consultation avec le bouton ajouter consultation | (3): et lorsque on va dans les détails d'une consultations



#Question14
--> Extention_README .md
