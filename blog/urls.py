from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('category/<slug:category_slug>/', views.category_posts, name='category_posts'),
    path('<slug:post_slug>/', views.post_detail, name='post_detail'),
]
