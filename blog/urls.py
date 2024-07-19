from django.urls import path
from .views import index, about, add_post, post_list


app_name = 'blog'
urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('post/add/', add_post, name='add_post'),
    path('post/', post_list, name='post_list'),
]
