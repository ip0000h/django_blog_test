from django.urls import path
from .views import (BlogList, BlogView, IndexView,
                    PostCreateView, PostDeleteView, PostUpdateView, PostView,
                    SubscriptionCreateView, SubscriptionDeleteView, PostMakeReadView)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('list/', BlogList.as_view(), name='list'),
    path('<int:blog_id>/', BlogView.as_view(), name='blog'),
    path('myposts/', BlogView.as_view(), name='myposts'),
    path('post/<int:pk>/', PostView.as_view(), name='post'),
    path('post/create/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('subscribe/<int:blog_id>/', SubscriptionCreateView.as_view(), name='subscribe'),
    path('unsubscribe/<int:blog_id>/', SubscriptionDeleteView.as_view(), name='unsubscribe'),
    path('post/<int:pk>/read', PostMakeReadView.as_view(), name='make-post-read'),
]
