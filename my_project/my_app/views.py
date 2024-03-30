# my_app/views.py
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import *
from .helper.simplexeMinimal import simplexe
import numpy as np
from .models import *
import json, math
from django.views.generic import TemplateView, ListView, DeleteView, DetailView, CreateView, UpdateView, FormView
from django.utils import timezone



def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                # Redirigez l'utilisateur vers la page d'édition de profil après la connexion réussie
                return redirect('home')
            else:
                # Gestion des erreurs si l'authentification échoue
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid email or password.'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile_edit')  # Redirection vers la même page après la mise à jour
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'profile_edit.html', {'form': form})

@login_required
def profile_detail(request):
    user = request.user
    return render(request, "profile.html", {'user': user})

class MedicineListView(ListView):
    model = Medicine
    template_name = "medicine_list.html"
    context_object_name = "medicine_list"

    def get_queryset(self):
        if self.kwargs["patient_id"]:
            patient = get_object_or_404(UserProfile, pk = self.kwargs["patient_id"])
            try:
                patientMedicines = PatientMedicine.objects.prefetch_related("medicine", "patient").filter(patient = patient.pk)
            except PatientMedicine.DoesNotExist:
                raise Http404("Mo medicines associated with this patient")
            return patientMedicines
        else:
            return Medicine.objects.all()

class Home(MedicineListView):
    model = Medicine
    template_name = "home.html"
    context_object_name = "medicine_list"
    def get_queryset(self):
        return Medicine.objects.all()
    
class MedicineCreateView(CreateView):
    template_name = "medicine_create.html"
    context_object_name = "medicine_create"
    success_url = "medicine_list"
    form_class = MedicineForm

    

class MedicineUpdateView(UpdateView):
    model = Medicine
    #form_class
    template_name = "medicine_update.html"
    context_object_name = "medicine_update"

class MedicineDetailView(DetailView):
    model = Medicine
    template_name = "medicine_detail.html"
    context_object_name = "medicine_detail"

    def get_context_data(self, **kwargs):
        #obtenir le context
        context = super().get_context_data(**kwargs)
        #ajouter la liste des symptomes
        list_symptome = []
        symptomes = get_list_or_404(MedicineSymptome, medicine = self.kwargs["pk"])
        for s in symptomes:
            list_symptome.append({"symptome":Symptome.objects.get(s.symptome), "efficacity":s.efficacity})
        context["list_symptome"] = list_symptome
        #retourner le contexte
        return context
    
class MedicineDeleteView(DeleteView):
    model = Medicine
    template_name = "delete_confirmation.html"
    context_object_name = "medicine"
    success_url = "medicine_list"

class SymptomeListView(ListView):
    model = Symptome
    template_name = "symptome_list.html"
    context_object_name = "symptome_list"

    def get_queryset(self):
        if self.kwargs["dangerousity"]:
            return Symptome.objects.filter(dangerousity = self.kwargs["dangerousity"])
        else :
            return Symptome.objects.all()
        
class SymptomeCreateView(CreateView):
    model = Symptome
    template_name = "symptome_create.html"
    context_object_name = "symptome_create"
    success_url = "symptome_list"
    form_class = SymptomeForm

class SymptomeUpdateView(UpdateView):
    model = Symptome
    template_name = "symptome_update.html"
    context_object_name = "symptome_update"

class SymptomeDetailView(DetailView):
    model = Symptome
    template_name = "symptome_detail.html"
    context_object_name = "symptome_detail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_medicine = []
        medicines = get_list_or_404(MedicineSymptome, symptome = self.kwargs["pk"])
        for m in medicines:
            list_medicine.append({"medicine":Medicine.objects.get(m.medicine), "efficacity":m.efficacity})
        context["list_medicine"] = list_medicine
        #retourner le contexte
        return context
    
class SymptomeDeleteView(DeleteView):
    model = Symptome
    template_name = "delete_confirmation.html"
    context_object_name = "symptome"
    success_url = "symptome_list"

#la consultation
class PatientSymptome(FormView):
    form_class = CurePatientForm
    template_name = "consultation.html"
    #success_url = "patient_cure.html"

    def form_valid(self, form):
        checkedSymptomes = form.cleaned_data['listSymptomField']
        symptomes = []
        for symptome in checkedSymptomes:
            symptomes.append(symptome.strip())
        
        symptomes_json = json.dumps(symptomes)
        cure_url = reverse("cure", kwargs={'symptomes': symptomes_json})
        return redirect (cure_url)

class CureView (TemplateView):
    template_name = "cure.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs["symptomes"]:
            data = json.loads(self.kwargs["symptomes"])
            symptomes1 = []
            for i in range (len(data)):
                symptomes1.append(Symptome.objects.get(name = data[i]))

            medicines = []
            for symptome in symptomes1:
                m = MedicineSymptome.objects.filter(symptome_id = symptome.id)
                for element in m:
                    if not element.medicine in medicines:
                        medicines.append(element.medicine)
            
            m = matrix(symptomes1, medicines)
            prix_quantite = simplexe(m) #prix et quantité des médicaments
            quantite = prix_quantite[1]
            cure = []
            i = 0
            for med in medicines:
                if quantite[i] > 0:
                    qtt = math.ceil(quantite[i])
                    cure.append({"med" : med, "qtt" : qtt, "prix": qtt*med.price})
                i+=1
            context["cure"] = cure
            return context

#view pour la facture
class BillView(CureView):
    template_name = "bill.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = get_object_or_404(UserProfile, pk = self.kwargs["patient"])
        cure = context["cure"]
        for key in cure:
            medicine = get_object_or_404(Medicine, name = key.strip())
            p = PatientMedicine()
            p.patient = patient 
            p.medicine = medicine
            p.quantity = cure[key]
            p.totalPrice = medicine.price * p.quantity
            p.dateOfPurchase = timezone.now()
            p.save()

        data = PatientMedicine.objects.prefetch_related("patient", "medicine").filter(patient = self.kwargs["patient"])
        context["bill"] = data
        return context

        

def matrix (symptomes, medicines):
    A = []
    l, m = len(symptomes), len(medicines)
    for symptome in symptomes:
        ligne = []
        for medicine in medicines:
            x = MedicineSymptome.objects.filter(medicine_id = medicine.id, symptome_id = symptome.id)
            if x:
                ligne.append(x[0].efficacity)
            else:
                ligne.append(0)
        A.append(ligne)

    #ajout des variables d'écart et des contraintes
    #variable artificielle t1, t2 et M tres grand = 100000
    M = 1000000
    i = 0
    for ligne in A:
        v_e = [0 for j in range(2*l)]
        v_e[i] = -1
        v_e[i+l] = 1
        ligne += v_e
        i+=1

    i = 0
    for symptome in symptomes:
        coeffs = [symptome.dangerousity, M]
        A[i] += coeffs
        i += 1
    
    #fonction à minimiser
    funct = [0 for j in range (len(A[0]))]
    i = 0
    for medicine in medicines:
        funct[i] = medicine.price
        i += 1

    for j in range (-(2+l), -2):
        funct[j] = M
    
    A.insert(0, funct)

    #remplacer zi et ci-zi par une liste de 0
    zi = [0 for i in range (len(A[0]))]
    ci_zi = [0 for i in range (len(A[0]))]
    A.append(zi)
    A.append(ci_zi)

    return np.array(A, dtype=np.float32)

