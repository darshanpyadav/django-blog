from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    # path('', views.index_view, name='blog_home'),
    path('', views.BlogListView.as_view(), name='blog_home'),
    path('post/<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),

    # path('posts/', views.post_list, name='post_list'),
    path('posts/', views.PostListView.as_view(), name='post_list'),

    # path('posts/create', views.post_create, name='blog-posts_create'),
    path('posts/create', views.PostCreateView.as_view(), name='post_create'),

    # path('posts/<int:pk>', views.post_detail, name='post_detail'),
    # path('posts/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<slug:slug>', views.PostDetailView.as_view(), name='post_detail'),

    # path('posts/<int:pk>/update', views.post_update, name='post_update'),
    # path('posts/<int:pk>/update', views.PostUpdateView.as_view(), name='post_update'),
    path('posts/<slug:slug>/update', views.PostUpdateView.as_view(), name='post_update'),

    # path('posts/<int:pk>/delete', views.post_delete, name='post_delete'),
    # path('posts/<int:pk>/delete', views.PostDeleteView.as_view(), name='post_delete'),
    path('posts/<slug:slug>/delete', views.PostDeleteView.as_view(), name='post_delete'),

    path('comments/<int:pk>/delete', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('comments/<int:pk>/approve', views.comment_approve, name='comment_approve')
]
