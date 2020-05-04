from django.urls import path
from .views import (PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, Home)
from . import views

urlpatterns = [
    path('', Home.as_view(), name='blog-home'),
    path('blog/', PostListView.as_view(), name='blog-page'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment-delete'),
    path('about/', views.about, name='blog-about'),
    path('like/<int:pk>/', views.like_post, name='like-post'),
    path('unlike/<int:pk>/', views.unlike_post, name='unlike-post'),
    path('search/', views.search, name='search'),
    path('thanks/', views.thanks, name='thanks'),
    path('newsletter/', views.newsletter, name='newsletter'),
]
