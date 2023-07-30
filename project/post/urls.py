from django.urls import path, include

from post.views import post_list, create_post, edit_post, delete_post, post_detail

app_name = 'post'

urlpatterns = [
    path('<str:category>', post_list, name='post_list'),
    path('<int:artist_pk>/create/', create_post, name='create_post'),
    path('<int:pk>/detail', post_detail, name='post_detail'),
    path('<int:pk>/edit', edit_post, name='post_edit'),
    path('<int:pk>/delete', delete_post, name='post_delete'),
]