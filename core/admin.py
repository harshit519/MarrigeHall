from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import (
    SiteSettings, HeroSection, AboutSection, Service, Facility,
    Venue, VenuePhoto, VenueVideo, Booking,
    CateringPackage, MenuCategory, MenuItem,
    Testimonial, Gallery, FAQ, BlogPost,
    Slider, Promotion, Event
)

# ============================================================================
# SITE SETTINGS & GENERAL CONTENT ADMIN
# ============================================================================

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'phone', 'email', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'site_tagline', 'logo', 'favicon')
        }),
        ('Contact Information', {
            'fields': ('address', 'phone', 'whatsapp', 'email')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url', 'youtube_url')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords')
        }),
        ('Footer', {
            'fields': ('footer_text', 'copyright_text')
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle', 'is_active', 'order', 'image_preview', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'subtitle']
    list_editable = ['is_active', 'order']
    
    def image_preview(self, obj):
        if obj.background_image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.background_image.url)
        return "No Image"
    image_preview.short_description = 'Background Image'
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'subtitle', 'description')
        }),
        ('Image & Button', {
            'fields': ('background_image', 'button_text', 'button_url')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )

@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle', 'is_active', 'image_preview', 'updated_at']
    list_filter = ['is_active', 'updated_at']
    search_fields = ['title', 'subtitle', 'content']
    list_editable = ['is_active']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image'
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'subtitle', 'content')
        }),
        ('Mission & Vision', {
            'fields': ('mission', 'vision')
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
    )

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'is_active', 'order', 'image_preview', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'order']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image'
    
    fieldsets = (
        ('Service Information', {
            'fields': ('name', 'description', 'icon')
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'is_active', 'order', 'image_preview', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'order']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image'
    
    fieldsets = (
        ('Facility Information', {
            'fields': ('name', 'description', 'icon')
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )

# ============================================================================
# VENUE & BOOKING ADMIN
# ============================================================================

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['name', 'venue_type', 'capacity', 'price', 'is_active', 'is_featured', 'created_at']
    list_filter = ['venue_type', 'is_active', 'is_featured', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'is_featured', 'price']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'venue_type', 'description', 'short_description')
        }),
        ('Pricing & Capacity', {
            'fields': ('capacity', 'price', 'price_per_hour')
        }),
        ('Details', {
            'fields': ('features', 'specifications')
        }),
        ('Settings', {
            'fields': ('is_active', 'is_featured')
        }),
    )

@admin.register(VenuePhoto)
class VenuePhotoAdmin(admin.ModelAdmin):
    list_display = ['venue', 'caption', 'is_primary', 'order', 'image_preview', 'created_at']
    list_filter = ['venue', 'is_primary', 'created_at']
    search_fields = ['venue__name', 'caption']
    list_editable = ['is_primary', 'order']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'
    
    fieldsets = (
        ('Photo Information', {
            'fields': ('venue', 'image', 'caption')
        }),
        ('Display Settings', {
            'fields': ('is_primary', 'order')
        }),
    )

@admin.register(VenueVideo)
class VenueVideoAdmin(admin.ModelAdmin):
    list_display = ['venue', 'title', 'video_type', 'is_active', 'order', 'created_at']
    list_filter = ['venue', 'is_active', 'created_at']
    search_fields = ['venue__name', 'title', 'description']
    list_editable = ['is_active', 'order']
    
    def video_type(self, obj):
        if obj.video_file:
            return "File Upload"
        elif obj.video_url:
            return "External URL"
        return "No Video"
    video_type.short_description = 'Video Type'
    
    fieldsets = (
        ('Video Information', {
            'fields': ('venue', 'title', 'description')
        }),
        ('Video Content', {
            'fields': ('video_file', 'video_url', 'thumbnail'),
            'description': 'Upload a video file or provide an external URL (YouTube/Vimeo)'
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'venue', 'event_type', 'event_date', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'event_date', 'venue', 'created_at']
    search_fields = ['user__username', 'venue__name', 'event_type']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('user', 'venue', 'event_type', 'event_date', 'start_time', 'end_time')
        }),
        ('Details', {
            'fields': ('guest_count', 'total_amount', 'special_requirements')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

# ============================================================================
# RESTAURANT & CATERING ADMIN
# ============================================================================

@admin.register(CateringPackage)
class CateringPackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_per_person', 'minimum_guests', 'maximum_guests', 'service_hours', 'is_featured', 'is_active']
    list_filter = ['is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_featured', 'is_active', 'price_per_person']
    
    fieldsets = (
        ('Package Information', {
            'fields': ('name', 'description', 'price_per_person')
        }),
        ('Requirements', {
            'fields': ('minimum_guests', 'maximum_guests', 'service_hours', 'features')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_active')
        }),
    )

@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'is_active', 'order', 'item_count']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'order']
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'
    
    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'description', 'icon')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_vegetarian', 'is_spicy', 'is_available', 'is_popular', 'image_preview', 'order']
    list_filter = ['category', 'is_vegetarian', 'is_spicy', 'is_available', 'is_popular', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'is_vegetarian', 'is_spicy', 'is_available', 'is_popular', 'order']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'
    
    fieldsets = (
        ('Item Information', {
            'fields': ('name', 'category', 'description', 'price')
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Options', {
            'fields': ('is_vegetarian', 'is_spicy', 'is_available', 'is_popular', 'order')
        }),
    )

# ============================================================================
# CONTENT & MARKETING ADMIN
# ============================================================================

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'author_title', 'rating', 'event_type', 'venue', 'is_featured', 'is_active', 'image_preview', 'created_at']
    list_filter = ['rating', 'is_featured', 'is_active', 'venue', 'created_at']
    search_fields = ['author_name', 'content']
    list_editable = ['rating', 'is_featured', 'is_active']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Author Image'
    
    fieldsets = (
        ('Author Information', {
            'fields': ('author_name', 'author_title', 'image')
        }),
        ('Testimonial Content', {
            'fields': ('content', 'rating')
        }),
        ('Event Details', {
            'fields': ('event_type', 'venue')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
    )

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'event_type', 'venue', 'is_featured', 'is_active', 'order', 'image_preview', 'created_at']
    list_filter = ['category', 'event_type', 'venue', 'is_featured', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_featured', 'is_active', 'order']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'
    
    fieldsets = (
        ('Image Information', {
            'fields': ('title', 'description', 'image')
        }),
        ('Categorization', {
            'fields': ('category', 'event_type', 'venue')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
    )

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'order', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['question', 'answer']
    list_editable = ['order', 'is_active']
    
    fieldsets = (
        ('FAQ Information', {
            'fields': ('question', 'answer', 'category')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'is_published', 'is_featured', 'published_at', 'featured_image_preview']
    list_filter = ['is_published', 'is_featured', 'category', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    list_editable = ['is_published', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    
    def featured_image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.featured_image.url)
        return "No Image"
    featured_image_preview.short_description = 'Featured Image'
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content', 'excerpt')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('Categorization', {
            'fields': ('category', 'tags')
        }),
        ('Publishing', {
            'fields': ('author', 'is_published', 'is_featured', 'published_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

# ============================================================================
# PROMOTIONAL ADMIN
# ============================================================================

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle', 'is_active', 'order', 'image_preview', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'subtitle']
    list_editable = ['is_active', 'order']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'subtitle')
        }),
        ('Image & Button', {
            'fields': ('image', 'button_text', 'button_url')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['title', 'discount_percentage', 'discount_amount', 'start_date', 'end_date', 'is_active', 'image_preview', 'created_at']
    list_filter = ['is_active', 'start_date', 'end_date', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_active']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'
    
    fieldsets = (
        ('Promotion Information', {
            'fields': ('title', 'description')
        }),
        ('Discount Details', {
            'fields': ('discount_percentage', 'discount_amount')
        }),
        ('Duration', {
            'fields': ('start_date', 'end_date')
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
    )

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_date', 'event_time', 'venue', 'is_active', 'image_preview', 'created_at']
    list_filter = ['event_date', 'venue', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_active']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'
    
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'description')
        }),
        ('Date & Time', {
            'fields': ('event_date', 'event_time')
        }),
        ('Venue', {
            'fields': ('venue',)
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
    )

# ============================================================================
# ADMIN SITE CUSTOMIZATION
# ============================================================================

# Customize admin site
admin.site.site_header = "Royal Palace Admin"
admin.site.site_title = "Royal Palace Admin Portal"
admin.site.index_title = "Welcome to Royal Palace Administration"

# Register models with custom admin classes
# (All models are already registered with @admin.register decorators above)
