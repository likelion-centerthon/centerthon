from django.urls import path, include

from post.views import post_list, create_post, edit_post, delete_post, post_detail, create_comment, delete_comment

app_name = 'post'

urlpatterns = [
    path('<int:artist_pk>/<str:category>/', post_list, name='post_list'),
    path('create/<int:artist_pk>/', create_post, name='create_post'),
    path('detail/<int:pk>/', post_detail, name='post_detail'),
    path('edit/<int:pk>/', edit_post, name='edit_post'),
    path('deletePost/<int:pk>/', delete_post, name='delete_post'),
    path('createComment/<int:pk>/', create_comment, name='create_comment'),
    path('deleteComment/<int:pk>/', delete_comment, name='delete_comment'),

]