from django.shortcuts import render, get_object_or_404
from .models import BlogCategory, BlogPost

def blog_list(request):
    """Display all published blog posts"""
    posts = BlogPost.objects.filter(is_published=True).order_by('-published_at', '-created_at')
    categories = BlogCategory.objects.filter(is_active=True)
    
    context = {
        'posts': posts,
        'categories': categories,
    }
    return render(request, 'blog/blog_list.html', context)

def category_posts(request, category_slug):
    """Display blog posts filtered by category"""
    category = get_object_or_404(BlogCategory, slug=category_slug, is_active=True)
    posts = BlogPost.objects.filter(category=category, is_published=True).order_by('-published_at')
    
    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'blog/category_posts.html', context)

def post_detail(request, post_slug):
    """Display detailed view of a blog post"""
    post = get_object_or_404(BlogPost, slug=post_slug, is_published=True)
    
    # Increment view count
    post.views += 1
    post.save()
    
    # Get related posts
    related_posts = BlogPost.objects.filter(
        category=post.category,
        is_published=True
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'blog/post_detail.html', context)
