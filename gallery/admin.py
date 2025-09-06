from django.contrib import admin
from .models import GalleryCategory, GalleryImage, GalleryVideo

@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'uploaded_at']
    list_filter = ['category', 'is_featured', 'uploaded_at']
    search_fields = ['title', 'description']
    list_editable = ['is_featured']
    date_hierarchy = 'uploaded_at'

@admin.register(GalleryVideo)
class GalleryVideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'uploaded_at']
    list_filter = ['category', 'is_featured', 'uploaded_at']
    search_fields = ['title', 'description']
    list_editable = ['is_featured']
    date_hierarchy = 'uploaded_at'
