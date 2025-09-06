from django.shortcuts import render, get_object_or_404
from .models import GalleryCategory, GalleryImage, GalleryVideo

def gallery(request):
    """Display gallery with all images and videos"""
    categories = GalleryCategory.objects.filter(is_active=True)
    images = GalleryImage.objects.all()
    videos = GalleryVideo.objects.all()
    
    context = {
        'categories': categories,
        'images': images,
        'videos': videos,
    }
    return render(request, 'gallery/gallery.html', context)

def category_gallery(request, category_id):
    """Display gallery filtered by category"""
    category = get_object_or_404(GalleryCategory, id=category_id, is_active=True)
    images = GalleryImage.objects.filter(category=category)
    videos = GalleryVideo.objects.filter(category=category)
    
    context = {
        'category': category,
        'images': images,
        'videos': videos,
    }
    return render(request, 'gallery/category_gallery.html', context)

def image_detail(request, image_id):
    """Display detailed view of an image"""
    image = get_object_or_404(GalleryImage, id=image_id)
    return render(request, 'gallery/image_detail.html', {'image': image})

def video_detail(request, video_id):
    """Display detailed view of a video"""
    video = get_object_or_404(GalleryVideo, id=video_id)
    return render(request, 'gallery/video_detail.html', {'video': video})
