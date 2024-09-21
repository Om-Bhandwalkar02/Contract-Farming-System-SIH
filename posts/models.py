from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    product = models.CharField(max_length=256)
    description = models.TextField(max_length=2048)
    price_per_unit = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    address = models.CharField(max_length=512)
    pincode = models.CharField(max_length=10)
    city = models.CharField(max_length=64)
    estimated_delivery_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product} by {self.author.full_name}'

    class Meta:
        ordering = ['-created_at']
