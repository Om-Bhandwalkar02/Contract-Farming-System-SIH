from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, HttpResponse
from .forms import FarmerSignupForm, BuyerSignupForm, LoginForm

# Farmer Signup
def farmer_signup(request):
    if request.method == 'POST':
        form = FarmerSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['pin'])
            user.role = 'farmer'
            user.save()
            return redirect('farmer_login')
    else:
        form = FarmerSignupForm()
    return render(request, 'users/signup.html', {'form': form, 'role': 'Farmer'})


# Buyer Signup
def buyer_signup(request):
    if request.method == 'POST':
        form = BuyerSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['pin'])
            user.role = 'buyer'
            user.save()
            return redirect('buyer_login')
    else:
        form = BuyerSignupForm()
    return render(request, 'users/signup.html', {'form': form, 'role': 'Buyer'})


# Farmer Login
def farmer_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('username')
            pin = form.cleaned_data.get('password')
            user = authenticate(request, username=phone_number, password=pin)
            if user is not None and user.role == 'farmer':
                login(request, user)
                return redirect('farmer_dashboard')
            else:
                form.add_error(None, 'Invalid credentials or role mismatch.')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form, 'role': 'Farmer'})


# Buyer Login
def buyer_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('username')
            pin = form.cleaned_data.get('password')
            user = authenticate(request, username=phone_number, password=pin)
            if user is not None and user.role == 'buyer':
                login(request, user)
                return redirect('buyer_dashboard')
            else:
                form.add_error(None, 'Invalid credentials or role mismatch.')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form, 'role': 'Buyer'})
