from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def index(request):
    return render(request, 'base/index.html')


def about(request):
    return render(request, 'base/about.html')


def feedback(request):
    return render(request, 'base/feedback.html')


def dashboard(request):
    return render(request, 'posts/post_list.html')
