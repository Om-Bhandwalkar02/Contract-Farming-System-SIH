from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def index(request):
    return render(request, 'base/index.html')


@login_required
def farmer_dashboard(request):
    return render(request, 'base/farmer_dashboard.html')


@login_required
def buyer_dashboard(request):
    return render(request, 'base/buyer_dashboard.html')
