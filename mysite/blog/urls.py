from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.PostView.as_view(), name='blog_post'),
    path('post/username/<str:username>/', views.PostView.as_view(), name='blog_post_by_user'),
    path('post/user/<int:user_id>/', views.PostView.as_view(), name='blog_post_by_user_id'),
    path('post/<int:id_>/', views.PostView.as_view(), name='blog_post_by_id'),
]
