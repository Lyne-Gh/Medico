from django.shortcuts import render
from .models import Consultation

def about(request):
    return render(request, 'medico/about.html')

def consultationDetail(request, consultationID):
    consultation=Consultation.objects.get(pk=consultationID)
    context = {
        "consultation": consultation,
    }
    return render(request,"medico/consultationDetails.html",context)
