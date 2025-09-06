from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils.text import slugify

# ============================================================================
# HOME PAGE & GENERAL CONTENT MODELS
# ============================================================================

class SiteSettings(models.Model):
    """Global site settings and configuration"""
    site_name = models.CharField(max_length=100, default="Royal Palace")
    site_tagline = models.CharField(max_length=200, blank=True)
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    favicon = models.ImageField(upload_to='site/', blank=True, null=True)
    
    # Contact Information
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    
    # Social Media
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    # SEO
    meta_description = models.TextField(blank=True)
    meta_keywords = models.TextField(blank=True)
    
    # Footer
    footer_text = models.TextField(blank=True)
    copyright_text = models.CharField(max_length=200, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return "Site Settings"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteSettings.objects.exists():
            return
        super().save(*args, **kwargs)

class HeroSection(models.Model):
    """Hero section content for homepage"""
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    background_image = models.ImageField(upload_to='hero/', blank=True, null=True)
    button_text = models.CharField(max_length=50, blank=True)
    button_url = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Sections"
    
    def __str__(self):
        return f"Hero: {self.title}"

class AboutSection(models.Model):
    """About section content"""
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    content = models.TextField()
    mission = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    image = models.ImageField(upload_to='about/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Sections"
    
    def __str__(self):
        return f"About: {self.title}"

class Service(models.Model):
    """Services offered by the venue"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class (e.g., fas fa-camera)")
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Service"
        verbose_name_plural = "Services"
    
    def __str__(self):
        return self.name

class Facility(models.Model):
    """Facilities available at the venue"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class")
    image = models.ImageField(upload_to='facilities/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Facilities"
    
    def __str__(self):
        return self.name

# ============================================================================
# VENUE & BOOKING MODELS
# ============================================================================

class Venue(models.Model):
    """Venue information"""
    VENUE_TYPES = [
        ('marriage_hall', 'Marriage Hall'),
        ('garden_lawn', 'Garden Lawn'),
        ('conference_room', 'Conference Room'),
        ('outdoor_space', 'Outdoor Space'),
    ]
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    venue_type = models.CharField(max_length=20, choices=VENUE_TYPES)
    description = models.TextField()
    short_description = models.CharField(max_length=200, blank=True)
    capacity = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    features = models.TextField(help_text="Enter features separated by commas")
    specifications = models.TextField(blank=True, help_text="Detailed specifications")
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "Venue"
        verbose_name_plural = "Venues"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class VenuePhoto(models.Model):
    """Photos for venues"""
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='venue_photos/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Venue Photo"
        verbose_name_plural = "Venue Photos"
    
    def __str__(self):
        return f"{self.venue.name} - {self.caption or 'Photo'}"

class VenueVideo(models.Model):
    """Videos for venues"""
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='venue_videos/', blank=True)
    video_url = models.URLField(blank=True, help_text="YouTube or Vimeo URL")
    thumbnail = models.ImageField(upload_to='venue_videos/thumbnails/', blank=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Venue Video"
        verbose_name_plural = "Venue Videos"
    
    def __str__(self):
        return f"{self.venue.name} - {self.title}"

class Booking(models.Model):
    """Booking information"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='core_bookings')
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=100)
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    guest_count = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requirements = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
    
    def __str__(self):
        return f"Booking {self.id} - {self.user.username} - {self.venue.name}"

# ============================================================================
# RESTAURANT & CATERING MODELS
# ============================================================================

class CateringPackage(models.Model):
    """Catering packages"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.TextField(help_text="Enter features separated by commas")
    minimum_guests = models.IntegerField()
    maximum_guests = models.IntegerField(blank=True, null=True)
    service_hours = models.IntegerField()
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['price_per_person']
        verbose_name = "Catering Package"
        verbose_name_plural = "Catering Packages"
    
    def __str__(self):
        return f"{self.name} - ₹{self.price_per_person}/person"

class MenuCategory(models.Model):
    """Menu categories"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon class")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Menu Category"
        verbose_name_plural = "Menu Categories"
    
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    """Menu items"""
    name = models.CharField(max_length=100)
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='items')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    is_vegetarian = models.BooleanField(default=False)
    is_spicy = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    is_popular = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['category', 'order', 'name']
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"
    
    def __str__(self):
        return f"{self.name} - ₹{self.price}"

# ============================================================================
# CONTENT & MARKETING MODELS
# ============================================================================

class Testimonial(models.Model):
    """Customer testimonials"""
    author_name = models.CharField(max_length=100)
    author_title = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    event_type = models.CharField(max_length=100, blank=True)
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
    
    def __str__(self):
        return f"{self.author_name} - {self.rating} stars"

class Gallery(models.Model):
    """Photo gallery"""
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='gallery/')
    category = models.CharField(max_length=50, blank=True)
    event_type = models.CharField(max_length=100, blank=True)
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Gallery Item"
        verbose_name_plural = "Gallery"
    
    def __str__(self):
        return self.title

class FAQ(models.Model):
    """Frequently asked questions"""
    question = models.CharField(max_length=200)
    answer = models.TextField()
    category = models.CharField(max_length=50, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'question']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
    
    def __str__(self):
        return self.question

class BlogPost(models.Model):
    """Blog posts for content marketing"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='core_blog_posts')
    category = models.CharField(max_length=50, blank=True)
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

# ============================================================================
# PROMOTIONAL MODELS
# ============================================================================

class Slider(models.Model):
    """Homepage slider"""
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='slider/')
    button_text = models.CharField(max_length=50, blank=True)
    button_url = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Slider"
        verbose_name_plural = "Sliders"
    
    def __str__(self):
        return self.title

class Promotion(models.Model):
    """Promotional offers and deals"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    discount_percentage = models.IntegerField(blank=True, null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='promotions/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Promotion"
        verbose_name_plural = "Promotions"
    
    def __str__(self):
        return f"{self.title} - {self.discount_percentage}% off"

class Event(models.Model):
    """Upcoming events"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateField()
    event_time = models.TimeField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['event_date', 'event_time']
        verbose_name = "Event"
        verbose_name_plural = "Events"
    
    def __str__(self):
        return f"{self.title} - {self.event_date}"
