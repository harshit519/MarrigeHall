from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('facilities/', views.facilities, name='facilities'),
    
    # Venues
    path('venues/', views.venues, name='venues'),
    path('venues/<slug:venue_slug>/', views.venue_detail, name='venue_detail'),
    
    # Restaurant & Catering
    path('catering/', views.catering, name='catering'),
    path('menu/', views.menu, name='menu'),
    
    # Content
    path('testimonials/', views.testimonials, name='testimonials'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:blog_slug>/', views.blog_detail, name='blog_detail'),
    path('faq/', views.faq, name='faq'),
    path('events/', views.events, name='events'),
]
