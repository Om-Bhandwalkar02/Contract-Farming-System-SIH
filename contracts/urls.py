from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_contract, name='create_contract'),
    path('detail/<int:contract_id>/', views.contract_detail, name='contract_detail'),
    path('sign/<int:contract_id>/', views.sign_contract, name='sign_contract'),
    path('list/', views.contract_list, name='contract_list'),
    path('check-farmer/', views.check_farmer_phone, name='check_farmer_phone'),
]
