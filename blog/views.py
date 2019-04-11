from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic
from .models import Post, Subscription


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'index.html'
    context_object_name = 'user_feed_list'

    def get_queryset(self):
        """Return the user feed posts ordered by date."""
        return Post.objects.filter(
            blog_id = self.kwargs['blog_id']
        ).order_by('-created').values()


class BlogView(LoginRequiredMixin, generic.ListView):
    template_name = 'blog.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """Return the user blog posts ordered by date."""
        return Post.objects.filter(
            blog_id = self.kwargs['blog_id']
        ).order_by('-created').values()


class BlogList(LoginRequiredMixin, generic.ListView):
    template_name = 'blogs.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        """Return the user blogs"""
        return settings.AUTH_USER_MODEL.objects.order_by('-created').values()


class PostView(LoginRequiredMixin, generic.DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
