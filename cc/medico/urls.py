from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('consultations/<int:consultationID>/',views.consultationDetail, name='consultationDetail' ),
    path('consultations/', views.consultations, name='listeconsultations'),
    path('nouvelle_consultation/', views.nouvelle_consultation, name='nouvelle_consultation'),
    path('effacer_consultation/<int:consultationID>/', views.deleteconsultation, name='deleteconsultation'),
    path('changer_consultation/<int:consultationID>/',views.editConsultation, name='editConsultation' ),
    
    path('modifier_traitement/<int:traitementID>', views.traitementModif, name='modifier_traitement'),
    path('traitement/<int:traitementID>/', views.traitementdetails, name='traitementdetails'),

    path('', views.main, name='main'), # URL pour la page principale
    path('ajouter_traitement/<int:consultation_id>/', views.ajouter_traitement, name='ajouter_traitement'),
    path('traitements/',views.traitements, name='listetraitements'),

    path('delete_traitement/<int:traitementID>/', views.delete_traitement, name='delete_traitement'), # URL pour supprimer un traitement
    path('consultation/<int:consultationID>/traitements/', views.suppression_traitement, name='suppression_traitement'), # URL page suppression traitements d'une consultation

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'), 
    path('add_doctor/', views.add_doctor, name='add_doctor'),
    path('appointments/', views.liste_rendez_vous, name='liste_rendez_vous'),
    path('takeappointments/', views.prendre_rendez_vous, name='prendre_rendez_vous'),
    path('doctors/', views.listdoctors, name='doctors'),
    path('editDoctor/<int:doctorID>', views.editDoctor, name='editDoctor'),
    path('deleteDoctor/<int:doctorID>', views.deleteDoctor, name='deleteDoctor'),
]
