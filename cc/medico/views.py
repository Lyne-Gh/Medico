from django.shortcuts import render ,redirect
from .forms import ConsultationForm
from .models import Consultation

def about(request):
    return render(request, 'medico/about.html')

def consultationDetail(request, consultationID):
    consultation=Consultation.objects.get(pk=consultationID)
    context = {
        "consultation": consultation,
    }
    return render(request,"medico/consultationDetails.html",context)

def consultations(request):
    lesConsultations = Consultation.objects.all().order_by('patient_nom')
    return render(request, 'medico/listeconsultations.html', {"lesConsultations":lesConsultations})

def nouvelle_consultation(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listeconsultations')  
    else:
        form = ConsultationForm()

    return render(request, 'medico/nouvelle_consultation.html', {'form': form})

