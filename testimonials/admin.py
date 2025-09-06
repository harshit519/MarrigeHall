from django.contrib import admin
from .models import Testimonial

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'event_type', 'rating', 'is_approved', 'is_featured', 'created_at']
    list_filter = ['rating', 'event_type', 'is_approved', 'is_featured', 'created_at']
    search_fields = ['name', 'title', 'review']
    list_editable = ['is_approved', 'is_featured']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
