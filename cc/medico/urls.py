from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('consultations/<int:consultationID>/',views.consultationDetail, name='consultationDetail' ),
    path('consultations/', views.consultations, name='listeconsultations'),
    path('nouvelle_consultation/', views.nouvelle_consultation, name='nouvelle_consultation'),
    path('effacer_consultation/<int:consultationID>/', views.deleteconsultation, name='deleteconsultation'),
    path('changer_consultation/<int:consultationID>/',views.editConsultation, name='editConsultation' ),
    
    # URL pour la page principale
    path('', views.main, name='main'),
    path('ajouter_traitement/<int:consultation_id>/', views.ajouter_traitement, name='ajouter_traitement'),
    path('traitements/',views.traitements, name='listetraitements'),


]
