from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from phonenumber_field.phonenumber import PhoneNumber
from .forms import ContractForm
from .models import Contract

User = get_user_model()


@login_required
def create_contract(request):
    if request.user.role != 'buyer':
        return redirect('index')

    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            contract = form.save(commit=False)
            contract.buyer = request.user
            farmer_contact = form.cleaned_data['farmer_contact']
            try:
                farmer = User.objects.get(contact=farmer_contact, role='farmer')
                contract.farmer = farmer
                contract.save()
                return redirect('contract_detail', contract_id=contract.id)
            except User.DoesNotExist:
                form.add_error('farmer_contact', 'Farmer with this contact does not exist.')
    else:
        form = ContractForm()
    return render(request, 'contracts/create_contract.html', {'form': form})


@login_required
def contract_detail(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    return render(request, 'contracts/contract_detail.html', {'contract': contract})


@login_required
def sign_contract(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    if contract.is_fully_signed():
        return redirect('contract_detail', contract_id=contract.id)  # If fully signed, no further signing allowed

    if request.user.role == 'farmer' and not contract.signed_by_farmer:
        contract.sign_contract(request.user)
    elif request.user.role == 'buyer' and contract.signed_by_farmer and not contract.signed_by_buyer:
        contract.sign_contract(request.user)

    return redirect('contract_detail', contract_id=contract.id)


@login_required
def contract_list(request):
    user = request.user
    if user.role == 'farmer':
        contracts = Contract.objects.filter(farmer=user).order_by('-created_at')
    elif user.role == 'buyer':
        contracts = Contract.objects.filter(buyer=user).order_by('-created_at')
    else:
        contracts = Contract.objects.none()

    return render(request, 'contracts/contract_list.html', {'contracts': contracts})


def check_farmer_phone(request):
    phone_number = request.GET.get('farmer_contact', '')

    response = "Farmer not exists"

    if phone_number:
        try:
            phone_number_obj = PhoneNumber.from_string(phone_number, region='IN')
            formatted_number = phone_number_obj.as_e164

            farmer = User.objects.filter(contact=formatted_number, role='farmer').first()
            if farmer:
                response = farmer.full_name
        except Exception as e:
            # exception for debugging
            print(f"Error: {e}")

    return HttpResponse(response)
