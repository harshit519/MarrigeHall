from django.urls import path
from . import views

app_name = 'testimonials'

urlpatterns = [
    path('', views.testimonial_list, name='testimonial_list'),
    path('add/', views.add_testimonial, name='add_testimonial'),
    path('<int:testimonial_id>/', views.testimonial_detail, name='testimonial_detail'),
]
