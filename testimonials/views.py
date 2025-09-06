from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Testimonial
from .forms import TestimonialForm

def testimonial_list(request):
    """Display all approved testimonials"""
    testimonials = Testimonial.objects.filter(is_approved=True).order_by('-created_at')
    return render(request, 'testimonials/testimonial_list.html', {'testimonials': testimonials})

def add_testimonial(request):
    """Add a new testimonial"""
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            testimonial = form.save()
            messages.success(request, 'Thank you for your testimonial! It will be reviewed and published soon.')
            return redirect('testimonials:testimonial_list')
    else:
        form = TestimonialForm()
    
    return render(request, 'testimonials/add_testimonial.html', {'form': form})

def testimonial_detail(request, testimonial_id):
    """Display detailed view of a testimonial"""
    testimonial = get_object_or_404(Testimonial, id=testimonial_id, is_approved=True)
    return render(request, 'testimonials/testimonial_detail.html', {'testimonial': testimonial})
