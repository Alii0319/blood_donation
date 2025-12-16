from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import DonorForm, RecipientForm, UserRegistrationForm, LoginForm
from .models import Donor, BloodRequest

# 🩸 Home Page
@login_required(login_url='login')
def home(request):
    return render(request, 'bloodbank/home.html')


# 🩸 User Login
def Login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"{username} logged in successfully!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'bloodbank/login.html', {'form': form})


# 🩸 User Logout
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('home')


# 🩸 User Registration
def userRegister_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created! You can now login.")
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'bloodbank/register.html', {'form': form})


# 🩸 Donor Registration
@login_required(login_url='login')
def register_donor(request):
    if request.method == 'POST':
        form = DonorForm(request.POST)
        if form.is_valid():
            if Donor.objects.filter(user=request.user).exists():
                messages.warning(request, "You are already registered as a donor.")
                return redirect('home')

            donor = form.save(commit=False)
            donor.user = request.user
            donor.save()
            messages.success(request, "Donor registered successfully!")
            return redirect('donor_success')
    else:
        form = DonorForm()
    return render(request, 'bloodbank/register_donor.html', {'form': form})


# 🩸 Donor Registration Success
def donor_success_view(request):
    return render(request, 'bloodbank/donor_success.html')


# 🩸 Find Donors
@login_required(login_url='login')
def find_donors(request):
    donors = []
    if request.method == 'POST':
        form = RecipientForm(request.POST)
        if form.is_valid():
            blood_group = form.cleaned_data['blood_group_needed']
            city = form.cleaned_data['city']
            donors = Donor.objects.filter(blood_group=blood_group, city__icontains=city, is_available=True)
    else:
        form = RecipientForm()
    return render(request, 'bloodbank/find_donors.html', {'form': form, 'donors': donors})


# 🩸 Send Blood Request (Recipient Side)
@login_required
def send_request(request, donor_id):
    donor = get_object_or_404(Donor, id=donor_id)

    if BloodRequest.objects.filter(recipient=request.user, donor=donor, status='Pending').exists():
        messages.warning(request, "You already sent a request to this donor.")
        return redirect('find_donors')

    BloodRequest.objects.create(recipient=request.user, donor=donor)
    messages.success(request, "Blood request sent successfully!")
    return redirect('find_donors')


# 🩸 Donor Requests View
@login_required
def donor_requests(request):
    requests = BloodRequest.objects.filter(donor__user=request.user).order_by('-request_date')
    return render(request, 'bloodbank/donor_requests.html', {'requests': requests})


# 🩸 Update Request Status (Accept/Reject)
@login_required
def update_request_status(request, request_id, status):
    blood_request = get_object_or_404(BloodRequest, id=request_id, donor__user=request.user)
    if status not in ['Accepted', 'Rejected']:
        messages.error(request, "Invalid status.")
        return redirect('donor_requests')

    blood_request.status = status
    blood_request.save()
    messages.success(request, f"Request {status.lower()} successfully.")
    return redirect('donor_requests')


# 🩸 Recipient Requests View
@login_required
def recipient_requests(request):
    requests = BloodRequest.objects.filter(recipient=request.user).order_by('-request_date')
    return render(request, 'bloodbank/recipient_requests.html', {'requests': requests})
