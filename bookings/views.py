from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Booking
from .forms import BookingForm
from core.models import Venue

def venue_list(request):
    venues = Venue.objects.filter(is_active=True)
    return render(request, 'bookings/venue_list.html', {'venues': venues})

def marriage_hall(request):
    return render(request, 'bookings/marriage_hall.html')

def garden_lawn(request):
    return render(request, 'bookings/garden_lawn.html')

def book_hall(request):
    return render(request, 'bookings/book_hall.html')

@login_required
def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, 'Booking created successfully!')
            return redirect('bookings:my_bookings')
    else:
        form = BookingForm()
    
    return render(request, 'bookings/create_booking.html', {'form': form})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})

@login_required
@require_POST
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.status = 'cancelled'
    booking.save()
    messages.success(request, 'Booking cancelled successfully!')
    return redirect('bookings:my_bookings')
