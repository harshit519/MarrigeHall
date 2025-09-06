from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_address', 'phone_number', 'special_instructions']
        widgets = {
            'delivery_address': forms.Textarea(attrs={'rows': 3}),
            'special_instructions': forms.Textarea(attrs={'rows': 3}),
        }
