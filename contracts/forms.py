from django import forms
from .models import Contract


class ContractForm(forms.ModelForm):
    farmer_contact = forms.CharField(max_length=20, label='Farmer Contact')

    class Meta:
        model = Contract
        fields = ['farmer_contact', 'product_name', 'quantity', 'price_per_unit',
                  'delivery_address', 'delivery_handler', 'delivery_date']

    def clean_farmer_contact(self):
        phone_number = self.cleaned_data['farmer_contact']
        # Ensure the phone number starts with +91, if not add it
        if not phone_number.startswith('+91'):
            phone_number = '+91' + phone_number
        # Strip any non-digit characters (optional)
        phone_number = ''.join(filter(str.isdigit, phone_number))
        # Format the phone number in E.164 format
        return f'+{phone_number}'
