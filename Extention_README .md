#Extension : Système d'authentification et gestion des médecins

Cette extension ajoute plusieurs fonctionnalités à l'application, y compris un système d'authentification, la gestion des médecins, un système de réservation d'appointments, ainsi qu'un calendrier pour visualiser les disponibilités.

#A/ Authentification:

L'application sera dotée d'un système d'authentification permettant aux utilisateurs de se connecter soit en tant qu'administrateur, soit en tant que médecin :

Administrateurs : Les administrateurs auront la possibilité d'ajouter de nouveaux médecins dans l'application.

Médecins : Les médecins pourront se connecter pour consulter et gérer leurs réservations.

#B/ Ajout de Modèle Médecin, patients et appointements


#C/ Système de Réservation:

Un système de réservation sera intégré permettant aux patients de réserver des rendez-vous en fonction des disponibilités des médecins. Les utilisateurs devront renseigner :

Le motif de la consultation : le patient peut spécifier la raison de la visite.

L'heure et la date : le système prendra en compte les plages horaires et les jours de disponibilité des médecins.

#D/ Liste des Médecins et de reservation

Permettant de voir l'ensemble des réservations pour un médecin spécifique.

Les médecins pourront également consulter leurs propres réservations et avoir une vue claire de leur emploi du temps.

#Pour se connecter en tant que admin (hardcoded):
'username': 'admin',
'password': 'admin/check'

#Pour se connecter en tant que docteur:
'username': 'Audrey',
'password': 'D000000'

#Pour se connecter en tant que patient:
'username': testmail@gmail.com
'password': 1234

Vous pouvez creer un compte en temps que patient.