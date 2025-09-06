from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Payment, PaymentGateway

@login_required
def process_payment(request):
    """Process payment for booking or order"""
    if request.method == 'POST':
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')
        booking_id = request.POST.get('booking_id')
        order_id = request.POST.get('order_id')
        
        # Create payment record
        payment = Payment.objects.create(
            user=request.user,
            amount=amount,
            payment_method=payment_method,
            status='pending'
        )
        
        # Redirect to payment gateway
        return redirect('payments:payment_success')
    
    return render(request, 'payments/process_payment.html')

def payment_success(request):
    """Handle successful payment"""
    messages.success(request, 'Payment completed successfully!')
    return render(request, 'payments/payment_success.html')

def payment_failed(request):
    """Handle failed payment"""
    messages.error(request, 'Payment failed. Please try again.')
    return render(request, 'payments/payment_failed.html')

def payment_webhook(request):
    """Handle payment gateway webhooks"""
    # Process webhook data from payment gateway
    return JsonResponse({'status': 'success'})
