from django import forms
from .models import Testimonial

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'email', 'event_type', 'rating', 'review', 'photo']
        widgets = {
            'review': forms.Textarea(attrs={'rows': 4}),
        }
