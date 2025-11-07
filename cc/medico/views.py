from django.shortcuts import render,redirect,get_object_or_404
from .forms import ConsultationForm,TraitementForm,DoctorForm, AppointmentForm
from .models import Consultation,Traitement,Doctor,Patient,Appointment
from django.contrib import messages
from datetime import datetime

def about(request):
    return render(request, 'medico/about.html')

def checkpermissions(request):
    if not (request.session.get('is_doctor') or request.session.get('is_admin')):
        return redirect('about')

def consultationDetail(request, consultationID):
    permission = checkpermissions(request)
    if permission:
        return permission
    consultation=Consultation.objects.get(pk=consultationID)
    lesTraitements = consultation.traitement_set.all()
    context = {
        "consultation": consultation,
        "lesTraitements": lesTraitements,
    }
    return render(request,"medico/consultationDetails.html",context)

def consultations(request):
    permission = checkpermissions(request)
    if permission:
        return permission
    lesConsultations = Consultation.objects.all().order_by('patient_nom')
    return render(request, 'medico/listeconsultations.html', {"lesConsultations":lesConsultations})

def nouvelle_consultation(request):
    permission = checkpermissions(request)
    if permission:
        return permission
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listeconsultations')  
    else:
        form = ConsultationForm()

    return render(request, 'medico/nouvelle_consultation.html', {'form': form})

def deleteconsultation(request, consultationID):
    permission = checkpermissions(request)
    if permission:
        return permission
    consultation = get_object_or_404(Consultation, pk=consultationID)

    if request.method == 'POST':
        consultation.delete()
        return redirect('listeconsultations')

    return render(request, "medico/consultationSupprConfirm.html", {"consultationid":consultationID})

def check_save(form,request):
    permission = checkpermissions(request)
    if permission:
        return permission
    if form.is_valid():
        consultation=form.save(commit=False)
        consultation.save()
    return consultation.id


def editConsultation(request,consultationID):
    permission = checkpermissions(request)
    if permission:
        return permission
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
    permission = checkpermissions(request)
    if permission:
        return permission
    traitement = get_object_or_404(Traitement, pk=traitementID)
    if(request.method == 'POST'):
        form = TraitementForm(request.POST,instance=traitement)
        traitementid = check_save(form, request)
        return redirect('traitementdetails', traitementID=traitementid)
    else:
        form=TraitementForm(instance=traitement)
    
    return render(request, "medico/traitementModif.html", {"form":form, "button_label":"modifier"})


def traitementdetails(request, traitementID):
    permission = checkpermissions(request)
    if permission:
        return permission
    traitement = get_object_or_404(Traitement, pk=traitementID)
    return render(request, 'medico/traitementdetails.html', {"traitement":traitement})


def main(request): # Vue pour la page principale
    return render(request, 'medico/main.html')

def ajouter_traitement(request, consultation_id):
    permission = checkpermissions(request)
    if permission:
        return permission
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
    permission = checkpermissions(request)
    if permission:
        return permission
    lesTraitements = Traitement.objects.all().order_by('medicament')
    return render(request, 'medico/listetraitement.html', {"lesTraitements":lesTraitements})


def suppression_traitement(request, consultationID): # Vue pour la page de suppression des traitements d'une consultation
    permission = checkpermissions(request)
    if permission:
        return permission
    consultation = get_object_or_404(Consultation, pk=consultationID)
    traitements = consultation.traitement_set.all()
    return render(request, "medico/suppression_traitement.html",{"consultation": consultation, 
                                                                          "traitements": traitements})
                                                                          


def delete_traitement(request, traitementID): # Vue pour supprimer un traitement
    permission = checkpermissions(request)
    if permission:
        return permission
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
                request.session['is_patient'] = False
                request.session['doctor_id'] = doctor.id
                return redirect('about')
            else:
                messages.error(request, 'Mot de passe incorrect.')
                return redirect('login')
        except Doctor.DoesNotExist:
            pass
        try:
            patient = Patient.objects.get(email=username)
            if patient.check_password(password):
                request.session['is_patient'] = True
                request.session['is_doctor'] = False
                request.session['is_admin'] = False
                request.session['patient_email'] = patient.email
                return redirect('about')
            else:
                messages.error(request, 'Mot de passe incorrect.')
                return redirect('login')
        except Patient.DoesNotExist:
            messages.error(request, "Nom d'utilisateur ou email incorrect.")

    return render(request, 'medico/login.html')

def logout_view(request):
    request.session.flush() 
    return redirect('about')

def add_doctor(request):
    permission = checkpermissions(request)
    if permission:
        return permission
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

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect('register')

        if Patient.objects.filter(email=email).exists():
            messages.error(request, "Un compte avec cet email existe déjà.")
            return redirect('register')

        patient = Patient(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )
        patient.save()
        messages.success(request, "Compte créé avec succès. Connectez-vous maintenant.")
        return redirect('login')

    return render(request, 'medico/register.html')

def prendre_rendez_vous(request):
    if not request.session.get('is_patient'):
        messages.error(request, "Vous devez être connecté comme patient pour prendre un rendez-vous.")
        return redirect('login')
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            patient_email = request.session.get('patient_email')
            try:
                patient = Patient.objects.get(email=patient_email)
            except Patient.DoesNotExist:
                messages.error(request, "Patient introuvable.")
                return redirect('login')
            appointment.patient = patient
            doctor = appointment.doctor
            try:
                start = datetime.strptime(doctor.start_time, '%H:%M').time()
                end = datetime.strptime(doctor.end_time, '%H:%M').time()
            except ValueError:
                messages.error(request, "Les horaires du docteur sont mal configurés.")
                return redirect('prendre_rendez_vous')
            if not (start <= appointment.appointment_time <= end):
                messages.error(request, f"Le docteur n'est pas disponible entre {doctor.start_time} et {doctor.end_time}.")
                return render(request, 'medico/prendre_rendez_vous.html', {'form': form})
            conflict = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=appointment.appointment_date,
                appointment_time=appointment.appointment_time
            ).exists()
            if conflict:
                messages.error(request, "Le docteur a déjà un rendez-vous à cette heure.")
                return render(request, 'medico/prendre_rendez_vous.html', {'form': form})
            appointment.save()
            messages.success(request, "Votre rendez-vous a été enregistré avec succès !")
            return redirect('liste_rendez_vous')

    else:
        form = AppointmentForm()

    return render(request, 'medico/prendre_rendez_vous.html', {'form': form})

def liste_rendez_vous(request):
    if request.session.get('is_patient'):
        email = request.session.get('patient_email')
        patient = Patient.objects.filter(email=email).first()
        if not patient:
            messages.error(request, "Patient introuvable.")
            return redirect('login')
        appointments = Appointment.objects.filter(patient=patient)
    elif request.session.get('is_doctor'):
        doctor_id = request.session.get('doctor_id')
        doctor = Doctor.objects.filter(id=doctor_id).first()
        if not doctor:
            messages.error(request, "Docteur introuvable.")
            return redirect('login')
        appointments = Appointment.objects.filter(doctor=doctor)
    else:
        messages.error(request, "Accès non autorisé.")
        return redirect('login')

    return render(request, 'medico/listerendezvous.html', {'appointments': appointments})

def listdoctors(request): 
    if not (request.session.get('is_admin')):
        return redirect('about')
    else:
        doctors = Doctor.objects.all() 
        return render(request, 'medico/doctordashboard.html', {'doctors':doctors})  
    
def editDoctor(request, doctorID):
    if not (request.session.get('is_admin')):
        return redirect('about')
    else:
        doctor = get_object_or_404(Doctor, pk=doctorID)
        if(request.method == 'POST'):
            form = DoctorForm(request.POST,instance=doctor)
            return redirect('doctor')
        else:
            form=DoctorForm(instance=doctor)
    
        return render(request, "medico/doctorModif.html", {"form":form, "button_label":"modifier"})

def deleteDoctor(request, doctorID):
    if not (request.session.get('is_admin')):
        return redirect('about')
    else:
        doctor = get_object_or_404(Doctor, pk=doctorID)
        doctor.delete()
        return redirect('doctors')