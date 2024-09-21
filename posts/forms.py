from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'product', 'description', 'price_per_unit', 'address', 'pincode', 'city',
                  'estimated_delivery_time']

        widgets = {
            'estimated_delivery_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
