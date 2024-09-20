from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Contract(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_contracts',
                              limit_choices_to={'role': 'buyer'})
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farmer_contracts',
                               limit_choices_to={'role': 'farmer'})

    product_name = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)  # Quantity in kg
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)  # Price per kg
    delivery_address = models.CharField(max_length=255)
    delivery_handler = models.CharField(max_length=255)
    delivery_date = models.DateField()

    signed_by_farmer = models.BooleanField(default=False)
    signed_by_buyer = models.BooleanField(default=False)
    farmer_signed_at = models.DateTimeField(null=True, blank=True)
    buyer_signed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def is_fully_signed(self):
        return self.signed_by_farmer and self.signed_by_buyer

    def sign_contract(self, user):
        if user.role == 'farmer':
            self.signed_by_farmer = True
            self.farmer_signed_at = timezone.now()
        elif user.role == 'buyer':
            self.signed_by_buyer = True
            self.buyer_signed_at = timezone.now()
        self.save()

    def __str__(self):
        return f"Contract: {self.product_name} between {self.farmer.full_name} and {self.buyer.full_name}"
