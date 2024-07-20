from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import PatientSignupForm, DoctorSignupForm
from .models import User, Patient, Doctor

def signup(request):
    if request.method == 'POST':
        form_type = request.POST.get('user_type')
        if form_type == 'patient':
            form = PatientSignupForm(request.POST, request.FILES)
        elif form_type == 'doctor':
            form = DoctorSignupForm(request.POST, request.FILES)
        else:
            form = None  # or handle invalid form_type if needed
        if form is not None and form.is_valid():
            user = form.save(commit=False)
            if form_type == 'patient':
                user.is_patient = True
            elif form_type == 'doctor':
                user.is_doctor = True
            user.save()
            profile = None
            if user.is_patient:
                profile = Patient(user=user, address=form.cleaned_data['address'], profile_picture=form.cleaned_data['profile_picture'])
            elif user.is_doctor:
                profile = Doctor(user=user, address=form.cleaned_data['address'], profile_picture=form.cleaned_data['profile_picture'])
            profile.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = PatientSignupForm()
    return render(request, 'index.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def dashboard(request):
    if request.user.is_patient:
        profile = Patient.objects.get(user=request.user)
    elif request.user.is_doctor:
        profile = Doctor.objects.get(user=request.user)
    return render(request, 'dashboard.html', {'profile': profile})
