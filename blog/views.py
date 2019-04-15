from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse, reverse_lazy
from .models import FeedPost, Post, Subscription


def post_after_save(sender, instance, create=True, **kwargs):
    """
    Create FeedPost instances and send notifications
    after creating new post
    """
    # get subscriptions
    subscriptions = Subscription.objects.filter(
        blog_id=instance.blog_id
    ).values_list('id', 'user_id')
    subscriptions_ids = [subscription[0] for subscription in subscriptions]
    # create FeedPost objects
    FeedPost.objects.bulk_create(
        [
            FeedPost(
                post_id=instance.id,
                subscription_id=subscription_id
            ) for subscription_id in subscriptions_ids
        ]
    )
    # sending emails
    user_ids = [subscription[1] for subscription in subscriptions]
    subscription_emails = get_user_model().objects.filter(
        id__in=user_ids
    ).values_list('email')
    subscription_emails = [subscription_email[0] for subscription_email in subscription_emails]
    send_mail(
        subject="New post from {}".format(instance.blog.username),
        message="{} {}{}".format(
            instance.title,
            settings.BASE_URL,
            reverse('post', kwargs={'pk': instance.id})
        ),
        from_email=settings.FROM_EMAIL,
        recipient_list=subscription_emails
    )

post_save.connect(post_after_save, sender=Post)


def subscription_after_save(sender, instance, create=True, **kwargs):
    """
    Create FeedPost instances after creating new subscription
    """
    # get subscriptions
    posts = Post.objects.filter(
        blog_id=instance.blog_id
    ).values_list('id')
    post_ids = [post[0] for post in posts]
    # create FeedPost objects
    FeedPost.objects.bulk_create(
        [
            FeedPost(
                post_id=post_id,
                subscription_id=instance.id
            ) for post_id in post_ids
        ]
    )

post_save.connect(subscription_after_save, sender=Subscription)


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """Return the user feed posts ordered by date."""
        posts = FeedPost.objects.select_related(
            'post',
        ).filter(
            subscription__user_id=self.request.user.id
        ).order_by('-post__created')
        return posts


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
        subscriptions = Subscription.objects.filter(
            user_id=self.request.user.id
        ).values_list(
            'blog_id'
        )
        subscriptions = [subscription[0] for subscription in subscriptions]
        blogs = get_user_model().objects.values(
            'id',
            'username',
        ).order_by(
            '-date_joined'
        )
        for blog in blogs:
            blog['is_subscribed'] = blog['id'] in subscriptions
        return blogs


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
        """Delete post and redirect to user's post page"""
        return self.post(request, *args, **kwargs)


class SubscriptionCreateView(LoginRequiredMixin, generic.RedirectView):
    pattern_name = 'list'

    def get_redirect_url(self, *args, **kwargs):
        """Save subscription and redirect to blog list page"""
        Subscription(
            blog_id=self.kwargs.get("blog_id"),
            user_id=self.request.user.id
        ).save()
        return super().get_redirect_url()


class SubscriptionDeleteView(LoginRequiredMixin, generic.RedirectView):
    pattern_name = 'list'

    def get_redirect_url(self, *args, **kwargs):
        """Delete subscription and redirect to blog list page"""
        get_object_or_404(
            Subscription,
            blog_id=self.kwargs.get("blog_id"),
            user_id=self.request.user.id
        ).delete()
        return super().get_redirect_url()


class PostMakeReadView(LoginRequiredMixin, generic.RedirectView):
    pattern_name = 'index'

    def get_redirect_url(self, *args, **kwargs):
        """Save subscription and redirect to blog list page"""
        feed_post = get_object_or_404(
            FeedPost,
            pk=self.kwargs.get("pk"),
        )
        feed_post.is_read = True
        feed_post.save()
        return super().get_redirect_url()
