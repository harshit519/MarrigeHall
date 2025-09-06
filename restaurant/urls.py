from django.urls import path
from . import views

app_name = 'restaurant'

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('catering/', views.catering, name='catering'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('place-order/', views.place_order, name='place_order'),
]
