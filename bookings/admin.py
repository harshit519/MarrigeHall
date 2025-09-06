from django.contrib import admin
from .models import Venue, Booking, TableBooking

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['name', 'venue_type', 'capacity', 'price_per_day', 'is_available']
    list_filter = ['venue_type', 'is_available']
    search_fields = ['name', 'description']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'venue', 'event_type', 'event_date', 'status', 'total_amount']
    list_filter = ['status', 'event_type', 'event_date', 'venue']
    search_fields = ['user__username', 'user__email', 'venue__name']
    date_hierarchy = 'event_date'
    readonly_fields = ['created_at', 'updated_at']

@admin.register(TableBooking)
class TableBookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'table_number', 'booking_date', 'booking_time', 'status']
    list_filter = ['status', 'booking_date']
    search_fields = ['user__username', 'user__email']
    date_hierarchy = 'booking_date'
