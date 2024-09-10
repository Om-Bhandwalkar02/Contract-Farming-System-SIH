from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import FarmerSignupForm, BuyerSignupForm, LoginForm, EditProfileForm


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


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(instance=request.user, data=request.POST, files=request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = EditProfileForm(instance=request.user, user=request.user)

    return render(request, 'users/edit_profile.html', {'form': form})


from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ChangePINForm


@login_required
def change_pin(request):
    if request.method == 'POST':
        form = ChangePINForm(request.POST)
        if form.is_valid():
            old_pin = form.cleaned_data['old_pin']
            new_pin = form.cleaned_data['new_pin']

            user = request.user

            if user.check_password(old_pin):
                user.set_password(new_pin)
                user.save()
                update_session_auth_hash(request, user)  # Keeps the user logged in after password change
                return redirect('index')  # Redirect to a success page or dashboard
            else:
                form.add_error('old_pin', 'Current PIN is incorrect.')
    else:
        form = ChangePINForm()

    return render(request, 'users/change_pin.html', {'form': form})

