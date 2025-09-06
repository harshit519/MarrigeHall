from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.venue_list, name='venue_list'),
    path('marriage-hall/', views.marriage_hall, name='marriage_hall'),
    path('garden-lawn/', views.garden_lawn, name='garden_lawn'),
    path('book-hall/', views.book_hall, name='book_hall'),
    path('create-booking/', views.create_booking, name='create_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
]
