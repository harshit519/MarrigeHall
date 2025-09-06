from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('process/', views.process_payment, name='process_payment'),
    path('success/', views.payment_success, name='payment_success'),
    path('failed/', views.payment_failed, name='payment_failed'),
    path('webhook/', views.payment_webhook, name='payment_webhook'),
]
