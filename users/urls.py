from django.urls import path
from . import views

urlpatterns = [
    path('farmer/signup/', views.farmer_signup, name='farmer_signup'),
    path('buyer/signup/', views.buyer_signup, name='buyer_signup'),
    path('farmer/login/', views.farmer_login, name='farmer_login'),
    path('buyer/login/', views.buyer_login, name='buyer_login'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change-pin/', views.change_pin, name='change_pin'),
    path('request-otp/<str:role>/', views.request_otp, name='request_otp'),
    path('verify-phone-number/', views.verify_phone_number, name='verify_phone_number'),
    path('check-phone/', views.check_phone_number, name='check_phone_number'),

]
