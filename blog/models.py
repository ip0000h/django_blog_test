from django.conf import settings
from django.db import models


class Post(models.Model):
    created = models.DateTimeField(
        'created', auto_now_add=True, db_index=True)
    blog = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='blog',
        on_delete=models.CASCADE, related_name='posts')
    title = models.CharField('title', max_length=255, db_index=True)
    post = models.TextField('post')

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        ordering = ('title',)
        unique_together = (
            ('blog', 'title'),
        )

    def __str__(self):
        return self.title


class Subscription(models.Model):
    blog = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='blog',
        on_delete=models.CASCADE, related_name='blog_subscriptions')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='user',
        on_delete=models.CASCADE, related_name='user_subscriptions')

    class Meta:
        unique_together = (
            ('blog', 'user'),
        )


class FeedPost(models.Model):
    post = models.ForeignKey(
        Post, verbose_name='post', on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='user',
        on_delete=models.CASCADE)
