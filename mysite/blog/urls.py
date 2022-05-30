from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.PostView.as_view(), name='blog_post'),
    path('post/<int:id_>', views.PostView.as_view(), name='blog_post_by_id'),
]
