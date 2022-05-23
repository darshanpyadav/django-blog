from django.urls import path
from . import views

app_name = "category"
urlpatterns = [
    path('', views.CategoryListView.as_view(), name='category_list'),
    path('create', views.category_create, name='category_create'),
    path('<int:pk>/delete', views.CategoryDelete.as_view(), name='category_delete'),
]