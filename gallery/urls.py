from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('category/<int:category_id>/', views.category_gallery, name='category_gallery'),
    path('image/<int:image_id>/', views.image_detail, name='image_detail'),
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),
]
