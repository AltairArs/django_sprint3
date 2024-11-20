from django.shortcuts import render, get_object_or_404
from .models import Category, Post
from django.utils import timezone
import pytz
# Create your views here.


def index(request):
    posts = Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    ).order_by('pub_date')[:5]
    template = 'blog/index.html'
    context = {'post_list': posts}
    return render(request, template, context)


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    if post.pub_date > timezone.now() or not post.is_published or not post.category.is_published:
        return render(request, '404.html', status=404)
    template = 'blog/detail.html'
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    if not category.is_published:
        return render(request, '404.html', status=404)
    posts = category.posts.select_related('location', 'category', 'author').filter(
        is_published=True,
        pub_date__lte=timezone.now()
    )
    template = 'blog/category.html'
    context = {
        'category': category,
        'post_list': posts
    }
    return render(request, template, context)
