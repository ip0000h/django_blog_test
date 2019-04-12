from django.urls import path
from .views import (BlogList, BlogView, IndexView, PostView,
                    SubscriptionList)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('list/', BlogList.as_view(), name='list'),
    path('subscriptions/', SubscriptionList.as_view(), name='subscriptions'),
    path('<int:blog_id>/', BlogView.as_view(), name='blog'),
    path('post/<int:pk>/', PostView.as_view(), name='post'),
    # path('subscribe/<int:blog_id>/', PostView.as_view(), name='subscribe'),
]
