from django.shortcuts import render, redirect
from .forms import DonorForm, RecipientForm, UserRegistrationForm, LoginForm
from .models import Donor
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# 🩸 Home Page (Login Required)
@login_required(login_url='login')
def home(request):
    return render(request, 'bloodbank/home.html')


# 🩸 Login View
def Login_view(request):
    if request.user.is_authenticated:  # ✅ prevent re-login
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"{username} has logged in successfully!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'bloodbank/login.html', {'form': form})


# 🩸 Logout View
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')


# 🩸 Register User
def userRegister_view(request):
    if request.user.is_authenticated:  # ✅ prevent re-register
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully! You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'bloodbank/register.html', {'form': form})


# 🩸 Register Donor (Login Required)
@login_required(login_url='login')
def register_donor(request):
    if request.method == 'POST':
        form = DonorForm(request.POST)
        if form.is_valid():
            if Donor.objects.filter(user=request.user).exists():
                messages.warning(request, 'You are already registered as a donor.')
                return redirect('home')  
            
            donor = form.save(commit=False)
            donor.user = request.user  
            donor.save()
            messages.success(request, 'Donor registered successfully!')
            return redirect('donor_success')
    else:
        form = DonorForm()
    
    return render(request, 'bloodbank/register_donor.html', {'form': form})


# 🩸 Donor Registration Success
def donor_success_view(request):
    return render(request, 'bloodbank/donor_success.html')


# 🩸 Find Donors (Login Required)
@login_required(login_url='login')
def find_donors(request):
    donors = []
    if request.method == 'POST':
        form = RecipientForm(request.POST)
        if form.is_valid():
            blood_group = form.cleaned_data['blood_group_needed']
            city = form.cleaned_data['city']
            donors = Donor.objects.filter(blood_group=blood_group, city__icontains=city)
    else:
        form = RecipientForm()
    
    return render(request, 'bloodbank/find_donors.html', {'form': form, 'donors': donors})
