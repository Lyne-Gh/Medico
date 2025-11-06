from django.shortcuts import render,redirect,get_object_or_404
from .forms import ConsultationForm,TraitementForm
from .models import Consultation,Traitement

def about(request):
    return render(request, 'medico/about.html')

def consultationDetail(request, consultationID):
    consultation=Consultation.objects.get(pk=consultationID)
    lesTraitements = consultation.traitement_set.all()
    context = {
        "consultation": consultation,
        "lesTraitements": lesTraitements,
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

def deleteconsultation(request, consultationID):
    consultation = get_object_or_404(Consultation, pk=consultationID)

    if request.method == 'POST':
        consultation.delete()
        return redirect('listeconsultations')

    return render(request, "medico/consultationSupprConfirm.html", {"consultationid":consultationID})
def check_save(form,request):
    if form.is_valid():
        consultation=form.save(commit=False)
        consultation.save()
    return consultation.id


def editConsultation(request,consultationID):
    consultation = get_object_or_404(Consultation,pk=consultationID)
    if request.method =="POST":
        form = ConsultationForm(request.POST,instance=consultation)
        id=check_save(form,request)
        return redirect("consultationDetail",consultationID=id)
    else:
        form=ConsultationForm(instance=consultation)
    return render(
        request,"medico/consultationModif.html",{"form": form, "button_label": "modifier"},
    )
# Vue pour la page principale
def main(request):
    return render(request, 'medico/main.html')

def ajouter_traitement(request, consultation_id):
    consultation = Consultation.objects.get(pk=consultation_id)


    if request.method == 'POST':
        form = TraitementForm(request.POST)
        if form.is_valid():
            traitement = form.save(commit=False)
            traitement.consultation = consultation #clé etrangere consultation
            traitement.save()
            return redirect('consultationDetail', consultationID=consultation.id)
    else:
        form = TraitementForm()


    return render(request, 'medico/ajouter_traitement.html', {'form': form, 'consultation': consultation})


def traitements(request):
    lesTraitements = Traitement.objects.all().order_by('medicament')
    return render(request, 'medico/listetraitement.html', {"lesTraitements":lesTraitements})
