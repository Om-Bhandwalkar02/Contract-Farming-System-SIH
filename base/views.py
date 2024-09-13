from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def index(request):
    return render(request, 'base/index.html')


def dashboard(request):
    return render(request, 'base/dashboard.html')

