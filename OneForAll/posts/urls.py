from django.urls import path
from .views import PostDeleteView,PostUpdateView, post_create_list_view, like_unlike_post, DeleteView

app_name = 'posts'

urlpatterns = [
    path('',post_create_list_view, name='main_post_view'),
    path('liked/',like_unlike_post, name='like_unlike_view'),
    path('<pk>/delete/',PostDeleteView.as_view(), name = 'post_delete'),
    path('<pk>/edit/',PostUpdateView.as_view(), name = 'post_edit'),
]