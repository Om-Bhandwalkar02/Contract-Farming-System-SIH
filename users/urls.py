from django.urls import path
from . import views

urlpatterns = [
    path('farmer/signup/', views.farmer_signup, name='farmer_signup'),
    path('buyer/signup/', views.buyer_signup, name='buyer_signup'),
    path('farmer/login/', views.farmer_login, name='farmer_login'),
    path('buyer/login/', views.buyer_login, name='buyer_login'),
]
