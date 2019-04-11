from django.urls import path
from .views import BlogList, BlogView, IndexView, PostView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('list/', BlogList.as_view(), name='list'),
    path('<int:blog_id>/', BlogView.as_view(), name='blog'),
    path('post/<int:pk>/', PostView.as_view(), name='post'),
]
