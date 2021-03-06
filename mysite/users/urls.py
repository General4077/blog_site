from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.Register.as_view(), name='users_register'),
    path('login/', views.Login.as_view(), name='users_login'),
    path('logout/', views.Logout.as_view(), name='users_logout'),
    path('profile/', views.Profile.as_view(), name='users_profile')
]
