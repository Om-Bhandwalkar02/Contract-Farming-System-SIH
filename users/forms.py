from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User


class FarmerSignupForm(forms.ModelForm):
    pin = forms.CharField(widget=forms.PasswordInput)
    pin_confirmation = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['full_name', 'contact', 'aadhar_number', 'farmer_certificate', 'address']

    def clean(self):
        cleaned_data = super().clean()
        pin = cleaned_data.get("pin")
        pin_confirmation = cleaned_data.get("pin_confirmation")

        if pin and pin != pin_confirmation:
            raise forms.ValidationError("The two PINs must match.")
        return cleaned_data


class BuyerSignupForm(forms.ModelForm):
    pin = forms.CharField(widget=forms.PasswordInput)
    pin_confirmation = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['full_name', 'contact', 'aadhar_number', 'buyer_certificate', 'address']

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