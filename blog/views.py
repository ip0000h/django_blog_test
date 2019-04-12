from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic
from .models import FeedPost, Post, Subscription


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'index.html'
    context_object_name = 'user_feed_list'

    def get_queryset(self):
        """Return the user feed posts ordered by date."""
        return Post.objects.filter(
            blog_id=self.kwargs['blog_id']
        ).order_by('-created').values()


class BlogView(LoginRequiredMixin, generic.ListView):
    template_name = 'blog.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """Return the user blog posts ordered by date."""
        return Post.objects.filter(
            blog_id=self.kwargs['blog_id']
        ).order_by('-created').values()


class BlogList(LoginRequiredMixin, generic.ListView):
    template_name = 'blogs.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        """Return the user blogs"""
        return get_user_model().objects.order_by('-date_joined').values()


class PostView(LoginRequiredMixin, generic.DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class SubscriptionList(LoginRequiredMixin, generic.ListView):
    template_name = 'subscriptions.html'
    context_object_name = 'subscriptions'

    def get_queryset(self):
        """Return the user blogs"""
        subs =  Subscription.objects.filter(user=self.request.user).select_related()
        print(subs, self.request.user)
        return subs