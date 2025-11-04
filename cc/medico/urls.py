from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('consultations/<int:consultationID>/',views.consultationDetail, name='consultationDetail' ),
    path('consultations/', views.consultations, name='listeconsultations'),
]
