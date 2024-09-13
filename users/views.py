from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash
from .forms import FarmerSignupForm, BuyerSignupForm, LoginForm, EditProfileForm, ChangePINForm
from django.contrib.auth.decorators import login_required
from twilio.rest import Client
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib import messages
import random
import phonenumbers

User = get_user_model()


def generate_otp():
    return random.randint(100000, 999999)


def send_otp(contact, otp):
    try:
        # phone number E.164 format
        parsed_number = phonenumbers.parse(contact, "IN")  # 'IN' for India; use the appropriate country code
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValueError("Invalid phone number format.")

        formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"Your OTP is {otp}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=formatted_number
        )
        return message.sid
    except Exception as e:
        raise ValueError(f"Failed to send OTP: {str(e)}")


def verify_phone_number(request):
    if request.method == 'POST':
        otp_input = request.POST.get('otp')

        stored_otp = request.session.get('otp')
        contact = request.session.get('contact')
        role = request.session.get('role')

        if str(otp_input) == str(stored_otp):
            request.session['is_verified'] = True
            messages.success(request, 'Phone number verified successfully!')

            # Redirect based on the role stored in the session
            if role == 'farmer':
                return redirect('farmer_signup')
            elif role == 'buyer':
                return redirect('buyer_signup')
        else:
            messages.error(request, 'Invalid OTP, please try again.')

    return render(request, 'users/verify_phone_number.html')


def request_otp(request, role):
    # Ensure the role is either 'farmer' or 'buyer'
    if role not in ['farmer', 'buyer']:
        return redirect('homepage')  # Redirect to homepage if an invalid role is provided

    if request.method == 'POST':
        contact = request.POST.get('contact')

        # Normalize the phone number by adding +91 if not present
        if contact and not contact.startswith('+91'):
            contact = '+91' + contact

        # Check if the phone number exists
        if User.objects.filter(contact=contact).exists():
            messages.warning(request, "Phone number already exists. Please login or use a different number.")
            return redirect('index')  # Replace with your login page URL

        else:
            otp = str(generate_otp())
            send_otp(contact, otp)

            # Save the OTP and contact in the session
            request.session['otp'] = otp
            request.session['contact'] = contact
            request.session['role'] = role

            return redirect('verify_phone_number')

    return render(request, 'users/request_otp.html')


# Farmer Signup
def farmer_signup(request):
    if not request.session.get('is_verified'):
        return redirect('request_otp', role='farmer')  # Redirect to OTP verification if not verified

    if request.method == 'POST':
        form = FarmerSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['pin'])
            user.role = 'farmer'
            # Assign contact number from session
            user.contact = request.session.get('contact')
            user.save()
            request.session.flush()  # Clear session after successful signup
            return redirect('farmer_login')
    else:
        form = FarmerSignupForm()
    return render(request, 'users/signup.html', {'form': form, 'role': 'Farmer'})


def buyer_signup(request):
    if not request.session.get('is_verified'):
        return redirect('request_otp', role='buyer')  # Redirect to OTP verification if not verified

    if request.method == 'POST':
        form = BuyerSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['pin'])
            user.role = 'buyer'
            # Assign contact number from session
            user.contact = request.session.get('contact')
            user.save()
            request.session.flush()  # Clear session after successful signup
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


def check_phone_number(request):
    phone_number = request.POST.get('contact', None)

    # Normalize the phone number by adding +91 if not present
    if phone_number and not phone_number.startswith('+91'):
        phone_number = '+91' + phone_number

    # Check if the phone number exists
    exists = User.objects.filter(contact=phone_number).exists()

    if exists:
        return HttpResponse("<p class='text-red-500 dark:text-red-300 text-xs italic'>Phone number already exists. "
                            "Please login.</p>"
                            "<script>document.querySelector('button[type=\"submit\"]').disabled = true;</script>")
    else:
        return HttpResponse("<p style='color:#16a34a' class='text-xs italic'>Phone number is available.</p>"
                            "<script>document.querySelector('button[type=\"submit\"]').disabled = false;</script>")
