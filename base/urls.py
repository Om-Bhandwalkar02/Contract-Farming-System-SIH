from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/farmer/dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
    path('users/buyer/dashboard/', views.buyer_dashboard, name='buyer_dashboard'),
]
