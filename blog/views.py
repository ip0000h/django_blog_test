from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from .models import FeedPost, Post, Subscription


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """Return the user feed posts ordered by date."""
        with transaction.atomic():
            user_subscriptions = Subscription.objects.values_list('blog').filter(
                user=self.request.user)
            return Post.objects.filter(
                blog__in=user_subscriptions
                ).order_by('-created').values()


class BlogView(LoginRequiredMixin, generic.ListView):
    template_name = 'blog.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """Return the user blog posts ordered by date."""
        blog_id = self.kwargs.get('blog_id') if self.kwargs.get('blog_id') else self.request.user.id
        return Post.objects.filter(
            blog_id=blog_id
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


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['title', 'post']
    template_name = 'post_form.html'
    success_url = reverse_lazy('myposts')

    def form_valid(self, form):
        form.instance.blog = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    fields = ['title', 'post']
    template_name = 'post_form.html'
    success_url = reverse_lazy('myposts')

    def get_object(self):
        """Return the Post instance that the view displays"""
        return get_object_or_404(
            Post,
            pk=self.kwargs.get("pk"),
            blog=self.request.user
        )


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy('myposts')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class SubscriptionList(LoginRequiredMixin, generic.ListView):
    template_name = 'subscriptions.html'
    context_object_name = 'subscriptions'

    def get_queryset(self):
        """Return the user's subscriptions"""
        return Subscription.objects.filter(
            user=self.request.user).select_related()
