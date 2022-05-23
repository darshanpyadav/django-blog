from django.urls import path
from . import views

app_name = "tag"
urlpatterns = [
    path('', views.TagListView.as_view(), name='tag_list'),
    path('create', views.tag_create, name='tag_create'),
    path('<int:pk>', views.TagDetailView.as_view(), name='tag_detail'),
    path('<int:pk>/update', views.TagUpdateView.as_view(), name='tag_update'),
    path('<int:pk>/delete', views.TagDelete.as_view(), name='tag_delete'),
]