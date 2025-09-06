from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from .models import (
    SiteSettings, HeroSection, AboutSection, Service, Facility,
    Venue, VenuePhoto, VenueVideo, Booking,
    CateringPackage, MenuCategory, MenuItem,
    Testimonial, Gallery, FAQ, BlogPost,
    Slider, Promotion, Event
)

def home(request):
    """Homepage with slider, sections, and highlights"""
    # Get site settings
    site_settings = SiteSettings.objects.first()
    
    # Get hero sections
    hero_sections = HeroSection.objects.filter(is_active=True)
    
    # Get sliders
    sliders = Slider.objects.filter(is_active=True)
    
    # Get services
    services = Service.objects.filter(is_active=True)[:6]
    
    # Get facilities
    facilities = Facility.objects.filter(is_active=True)[:6]
    
    # Get featured venues
    featured_venues = Venue.objects.filter(is_active=True, is_featured=True)[:3]
    
    # Get testimonials
    testimonials = Testimonial.objects.filter(is_active=True, is_featured=True)[:6]
    
    # Get gallery images
    gallery_images = Gallery.objects.filter(is_active=True, is_featured=True)[:8]
    
    # Get latest blog posts
    latest_posts = BlogPost.objects.filter(is_published=True)[:3]
    
    # Get active promotions
    promotions = Promotion.objects.filter(is_active=True)[:3]
    
    # Provide compatibility aliases for existing templates
    sections = hero_sections
    packages = CateringPackage.objects.filter(is_active=True)[:3]
    featured_images = gallery_images
    
    context = {
        'site_settings': site_settings,
        'hero_sections': hero_sections,
        'sections': sections,
        'sliders': sliders,
        'services': services,
        'facilities': facilities,
        'featured_venues': featured_venues,
        'testimonials': testimonials,
        'gallery_images': gallery_images,
        'featured_images': featured_images,
        'latest_posts': latest_posts,
        'promotions': promotions,
        'packages': packages,
    }
    return render(request, 'core/home.html', context)

def about(request):
    """About us page with history, mission, and facilities"""
    # Get site settings
    site_settings = SiteSettings.objects.first()
    
    # Get about section
    about_section = AboutSection.objects.filter(is_active=True).first()
    
    # Get services
    services = Service.objects.filter(is_active=True)
    
    # Get facilities
    facilities = Facility.objects.filter(is_active=True)
    
    # Get testimonials
    testimonials = Testimonial.objects.filter(is_active=True)[:4]
    
    # Compatibility alias
    about = about_section
    
    context = {
        'site_settings': site_settings,
        'about_section': about_section,
        'about': about,
        'services': services,
        'facilities': facilities,
        'testimonials': testimonials,
    }
    return render(request, 'core/about.html', context)

def contact(request):
    """Contact page with form, map, and contact info"""
    # Get site settings for contact info
    site_settings = SiteSettings.objects.first()
    contact_info = site_settings  # compatibility alias
    
    if request.method == 'POST':
        # Handle contact form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Here you would typically send an email
        # For now, we'll just show a success message
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        
    context = {
        'site_settings': site_settings,
        'contact_info': contact_info,
    }
    return render(request, 'core/contact.html', context)

def venues(request):
    """Venues listing page"""
    # Simple handoff to static venue list page used in bookings app
    return render(request, 'bookings/venue_list.html')

def venue_detail(request, venue_slug):
    """Individual venue detail page"""
    # Get site settings
    site_settings = SiteSettings.objects.first()
    
    # Get venue
    venue = get_object_or_404(Venue, slug=venue_slug, is_active=True)
    
    # Get venue photos
    photos = VenuePhoto.objects.filter(venue=venue).order_by('order')
    
    # Get venue videos
    videos = VenueVideo.objects.filter(venue=venue, is_active=True).order_by('order')
    
    # Get related venues
    related_venues = Venue.objects.filter(
        venue_type=venue.venue_type, 
        is_active=True
    ).exclude(id=venue.id)[:3]
    
    # Get testimonials for this venue
    venue_testimonials = Testimonial.objects.filter(
        venue=venue, 
        is_active=True
    )[:3]
    
    context = {
        'site_settings': site_settings,
        'venue': venue,
        'photos': photos,
        'videos': videos,
        'related_venues': related_venues,
        'venue_testimonials': venue_testimonials,
    }
    return render(request, 'core/venue_detail.html', context)

def facilities(request):
    """Facilities page with all amenities"""
    # Get site settings
    site_settings = SiteSettings.objects.first()
    
    # Get all facilities
    facilities = Facility.objects.filter(is_active=True)
    
    # Get services
    services = Service.objects.filter(is_active=True)
    
    context = {
        'site_settings': site_settings,
        'facilities': facilities,
        'services': services,
    }
    return render(request, 'core/facilities.html', context)

def catering(request):
    """Catering packages page"""
    # Get site settings
    site_settings = SiteSettings.objects.first()
    
    # Get catering packages
    packages = CateringPackage.objects.filter(is_active=True)
    
    # Get menu categories
    menu_categories = MenuCategory.objects.filter(is_active=True)
    
    # Get popular menu items
    popular_items = MenuItem.objects.filter(is_active=True, is_popular=True)
    
    context = {
        'site_settings': site_settings,
        'packages': packages,
        'menu_categories': menu_categories,
        'popular_items': popular_items,
    }
    return render(request, 'core/catering.html', context)

def menu(request):
    """Restaurant menu page"""
    # Get site settings
    site_settings = SiteSettings.objects.first()
    
    # Get menu categories with items
    categories = MenuCategory.objects.filter(is_active=True).prefetch_related('items')
    
    # Get all menu items
    menu_items = MenuItem.objects.filter(is_active=True)
    
    # Handle filtering
    category_id = request.GET.get('category')
    if category_id:
        menu_items = menu_items.filter(category_id=category_id)
    
    # Handle search
    search_query = request.GET.get('search')
    if search_query:
        menu_items = menu_items.filter(name__icontains=search_query)
    
    # Handle dietary filters
    vegetarian = request.GET.get('vegetarian')
    if vegetarian:
        menu_items = menu_items.filter(is_vegetarian=True)
    
    spicy = request.GET.get('spicy')
    if spicy:
        menu_items = menu_items.filter(is_spicy=True)
    
    context = {
        'site_settings': site_settings,
        'categories': categories,
        'menu_items': menu_items,
        'selected_category': category_id,
        'search_query': search_query,
    }
    return render(request, 'core/menu.html', context)

def gallery(request):
    """Photo gallery page"""
    # Get site settings
    site_settings = SiteSettings.objects.first()
    
    # Get gallery images
    images = Gallery.objects.filter(is_active=True)
    
    # Handle filtering
    category = request.GET.get('category')
    if category:
        images = images.filter(category=category)
    
    event_type = request.GET.get('event_type')
    if event_type:
        images = images.filter(event_type=event_type)
    
    # Pagination
    paginator = Paginator(images, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get unique categories and event types for filtering
    categories = Gallery.objects.filter(is_active=True).values_list('category', flat=True).distinct()
    event_types = Gallery.objects.filter(is_active=True).values_list('event_type', flat=True).distinct()
    
    context = {
        'site_settings': site_settings,
        'page_obj': page_obj,
        'categories': categories,
        'event_types': event_types,
        'selected_category': category,
        'selected_event_type': event_type,
    }
    return render(request, 'core/gallery.html', context)

def testimonials(request):
    """Testimonials page"""
    # Get site settings
    site_settings = SiteSettings.objects.first()
    
    # Get testimonials
    testimonials = Testimonial.objects.filter(is_active=True)
    
    # Handle filtering
    venue_id = request.GET.get('venue')
    if venue_id:
        testimonials = testimonials.filter(venue_id=venue_id)
    
    rating = request.GET.get('rating')
    if rating:
        testimonials = testimonials.filter(rating=rating)
    
    # Pagination
    paginator = Paginator(testimonials, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get venues for filtering
    venues = Venue.objects.filter(is_active=True)
    
    context = {
        'site_settings': site_settings,
        'page_obj': page_obj,
        'venues': venues,
        'selected_venue': venue_id,
        'selected_rating': rating,
    }
    return render(request, 'core/testimonials.html', context)

def blog(request):
    """Blog listing page"""
    # Get site settings
    site_settings = SiteSettings.objects.first()
    
    # Get published blog posts
    posts = BlogPost.objects.filter(is_published=True)
    
    # Handle search
    search_query = request.GET.get('search')
    if search_query:
        posts = posts.filter(title__icontains=search_query)
    
    # Handle category filter
    category = request.GET.get('category')
    if category:
        posts = posts.filter(category=category)
    
    # Pagination
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories for filtering
    categories = BlogPost.objects.filter(is_published=True).values_list('category', flat=True).distinct()
    
    context = {
        'site_settings': site_settings,
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category,
    }
    return render(request, 'core/blog.html', context)

def blog_detail(request, blog_slug):
    """Individual blog post detail page"""
    # Get site settings
    site_settings = SiteSettings.objects.first()
    
    # Get blog post
    post = get_object_or_404(BlogPost, slug=blog_slug, is_published=True)
    
    # Get related posts
    related_posts = BlogPost.objects.filter(
        category=post.category,
        is_published=True
    ).exclude(id=post.id)[:3]
    
    context = {
        'site_settings': site_settings,
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'core/blog_detail.html', context)

def faq(request):
    """FAQ page"""
    # Get site settings
    site_settings = SiteSettings.objects.first()
    
    # Get FAQs
    faqs = FAQ.objects.filter(is_active=True)
    
    # Group by category
    faq_categories = {}
    for faq in faqs:
        category = faq.category or 'General'
        if category not in faq_categories:
            faq_categories[category] = []
        faq_categories[category].append(faq)
    
    context = {
        'site_settings': site_settings,
        'faq_categories': faq_categories,
    }
    return render(request, 'core/faq.html', context)

def events(request):
    """Upcoming events page"""
    # Get site settings
    site_settings = SiteSettings.objects.first()
    
    # Get upcoming events
    events = Event.objects.filter(is_active=True)
    
    # Handle venue filter
    venue_id = request.GET.get('venue')
    if venue_id:
        events = events.filter(venue_id=venue_id)
    
    # Get venues for filtering
    venues = Venue.objects.filter(is_active=True)
    
    context = {
        'site_settings': site_settings,
        'events': events,
        'venues': venues,
        'selected_venue': venue_id,
    }
    return render(request, 'core/events.html', context)
