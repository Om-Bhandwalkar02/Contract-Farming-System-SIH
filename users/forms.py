from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User


def validate_pin_length(value):
    if len(value) != 6:
        raise ValidationError('PIN must be exactly 6 digits.')


class FarmerSignupForm(forms.ModelForm):
    pin = forms.CharField(widget=forms.PasswordInput, validators=[validate_pin_length])
    pin_confirmation = forms.CharField(widget=forms.PasswordInput, validators=[validate_pin_length])

    class Meta:
        model = User
        fields = ['full_name', 'aadhar_number', 'farmer_certificate', 'address']

    def clean(self):
        cleaned_data = super().clean()
        pin = cleaned_data.get("pin")
        pin_confirmation = cleaned_data.get("pin_confirmation")

        if pin and pin != pin_confirmation:
            raise forms.ValidationError("The two PINs must match.")
        return cleaned_data


class BuyerSignupForm(forms.ModelForm):
    pin = forms.CharField(widget=forms.PasswordInput, validators=[validate_pin_length])
    pin_confirmation = forms.CharField(widget=forms.PasswordInput, validators=[validate_pin_length])

    class Meta:
        model = User
        fields = ['full_name', 'aadhar_number', 'buyer_certificate', 'address']

    def clean(self):
        cleaned_data = super().clean()
        pin = cleaned_data.get("pin")
        pin_confirmation = cleaned_data.get("pin_confirmation")

        if pin and pin != pin_confirmation:
            raise forms.ValidationError("The two PINs must match.")
        return cleaned_data


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Phone Number", widget=forms.TextInput())
    password = forms.CharField(label="PIN", widget=forms.PasswordInput())

    # Override the clean_username method to preprocess the phone number
    def clean_username(self):
        phone_number = self.cleaned_data['username']

        if not phone_number.startswith('+91'):
            phone_number = '+91' + phone_number

        return phone_number


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'full_name', 'address', 'profile_picture',
            'aadhar_certificate', 'farmer_certificate', 'buyer_certificate'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EditProfileForm, self).__init__(*args, **kwargs)

        # Remove certificate fields based on the user's role
        if user and user.role == 'farmer':
            self.fields.pop('buyer_certificate')
        elif user and user.role == 'buyer':
            self.fields.pop('farmer_certificate')


class ChangePINForm(forms.Form):
    old_pin = forms.CharField(widget=forms.PasswordInput, label='Current PIN', validators=[validate_pin_length])
    new_pin = forms.CharField(widget=forms.PasswordInput, label='New PIN', validators=[validate_pin_length])
    new_pin_confirmation = forms.CharField(widget=forms.PasswordInput, label='Confirm New PIN')

    def clean(self):
        cleaned_data = super().clean()
        old_pin = cleaned_data.get("old_pin")
        new_pin = cleaned_data.get("new_pin")
        new_pin_confirmation = cleaned_data.get("new_pin_confirmation")

        if new_pin and new_pin != new_pin_confirmation:
            raise forms.ValidationError("The new PINs must match.")

        return cleaned_data
