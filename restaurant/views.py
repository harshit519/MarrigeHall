from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import MenuItem, Order
from .forms import OrderForm
from core.models import CateringPackage

def menu(request):
    menu_items = MenuItem.objects.filter(is_available=True).order_by('category', 'order')
    return render(request, 'restaurant/menu.html', {'menu_items': menu_items})

def catering(request):
    catering_packages = CateringPackage.objects.filter(is_active=True)
    return render(request, 'restaurant/catering.html', {'catering_packages': catering_packages})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'restaurant/my_orders.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'restaurant/order_detail.html', {'order': order})

@login_required
def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            messages.success(request, 'Order placed successfully!')
            return redirect('restaurant:my_orders')
    else:
        form = OrderForm()
    
    return render(request, 'restaurant/place_order.html', {'form': form})
