from django.shortcuts import render,redirect,get_object_or_404
from .forms import ConsultationForm,TraitementForm,DoctorForm
from .models import Consultation,Traitement,Doctor
from django.contrib import messages

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

def traitementModif(request, traitementID):
    traitement = get_object_or_404(Traitement, pk=traitementID)
    if(request.method == 'POST'):
        form = TraitementForm(request.POST,instance=traitement)
        traitementid = check_save(form, request)
        return redirect('traitementdetails', traitementID=traitementid)
    else:
        form=TraitementForm(instance=traitement)
    
    return render(request, "medico/traitementModif.html", {"form":form, "button_label":"modifier"})


def traitementdetails(request, traitementID):
    traitement = get_object_or_404(Traitement, pk=traitementID)
    return render(request, 'medico/traitementdetails.html', {"traitement":traitement})


def main(request): # Vue pour la page principale
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


def suppression_traitement(request, consultationID): # Vue pour la page de suppression des traitements d'une consultation
    consultation = get_object_or_404(Consultation, pk=consultationID)
    traitements = consultation.traitement_set.all()
    return render(request, "medico/suppression_traitement.html",{"consultation": consultation, 
                                                                          "traitements": traitements})
                                                                          


def delete_traitement(request, traitementID): # Vue pour supprimer un traitement
    traitement = get_object_or_404(Traitement, pk=traitementID)
    consultation_id = traitement.consultation.id

    if request.method == 'POST':
        traitement.delete()
        return redirect('suppression_traitement', consultationID=consultation_id)

    return render(request, "medico/traitementSupprConfirm.html", {"traitementID":traitementID})

ADMIN_CREDENTIALS = {
    'username': 'admin',
    'password': 'admin/check'
}

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == ADMIN_CREDENTIALS['username'] and password == ADMIN_CREDENTIALS['password']:
            request.session['is_admin'] = True
            request.session['is_doctor'] = False
            return redirect('about')
        try:
            doctor = Doctor.objects.get(first_name=username)  
            if doctor.check_password(password): 
                request.session['is_doctor'] = True
                request.session['is_admin'] = False
                return redirect('about')  
            else:
                messages.error(request, 'Mot de passe incorrect.')
        except Doctor.DoesNotExist:
            messages.error(request, 'Nom d\'utilisateur incorrect.')

    return render(request, 'medico/login.html')

def logout_view(request):
    request.session.flush() 
    return redirect('about')

def add_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():

            doctor = form.save()
            if doctor.shift == 'morning':
                doctor.start_time = '08:00'
                doctor.end_time = '17:00'
            elif doctor.shift == 'night':
                doctor.start_time = '17:00'
                doctor.end_time = '08:00'

            doctor.save()
            doctor.available_days = ', '.join(form.cleaned_data['available_days'])
            doctor.save()

            messages.success(request, "Médecin ajouté avec succès!")
            return redirect('about')  

    else:
        form = DoctorForm()

    return render(request, 'medico/add_doctor.html', {'form': form})