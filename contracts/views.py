from django.http import HttpResponse
from django.shortcuts import render


def contract(request):
    return HttpResponse("Hello World")
