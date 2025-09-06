from django.db import models
from django.contrib.auth.models import User
from bookings.models import Booking
from restaurant.models import Order

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('razorpay', 'Razorpay'),
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        ('upi', 'UPI'),
        ('cash', 'Cash'),
        ('card', 'Credit/Debit Card'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    gateway_response = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return f"Payment {self.transaction_id} - {self.user.username}"

class PaymentGateway(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    api_key = models.CharField(max_length=200, blank=True)
    secret_key = models.CharField(max_length=200, blank=True)
    webhook_url = models.URLField(blank=True)
    
    def __str__(self):
        return self.name
