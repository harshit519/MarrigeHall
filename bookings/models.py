from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Venue(models.Model):
    VENUE_TYPES = [
        ('hall', 'Marriage Hall'),
        ('lawn', 'Garden Lawn'),
        ('restaurant', 'Restaurant'),
    ]
    
    name = models.CharField(max_length=100)
    venue_type = models.CharField(max_length=20, choices=VENUE_TYPES)
    capacity = models.IntegerField(help_text="Maximum number of guests")
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='venues/', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    amenities = models.TextField(help_text="List of amenities available")
    
    def __str__(self):
        return f"{self.name} ({self.get_venue_type_display()})"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    EVENT_TYPES = [
        ('wedding', 'Wedding'),
        ('birthday', 'Birthday Party'),
        ('corporate', 'Corporate Event'),
        ('reception', 'Reception'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    number_of_guests = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    advance_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    special_requirements = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.venue.name} on {self.event_date}"
    
    def is_past_event(self):
        return self.event_date < timezone.now().date()
    
    def is_today(self):
        return self.event_date == timezone.now().date()

class TableBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table_number = models.IntegerField()
    booking_date = models.DateField()
    booking_time = models.TimeField()
    number_of_guests = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Table {self.table_number} - {self.user.username} on {self.booking_date}"
