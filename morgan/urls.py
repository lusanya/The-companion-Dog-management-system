from django.urls import path

# morgan/urls.py

from django.urls import path
from . import views  # Import views from the current app (morgan)
from django.contrib.auth import views as auth_views

from .views import password_reset, password_reset_confirm

urlpatterns = [
    path('', views.login_page, name='login'),
    path('home/', views.home, name='home'),
    path('register/',views.register_page,name='register'),
    path('logout/',views.logout_page,name='logout'),
    path('password_reset/', password_reset, name='password_reset'),
    path('password_reset_confirm/', password_reset_confirm, name='password_reset_confirm'),
    path('dogs/',views.dog_profiles,name='dog_profiles'),
    path('add_dog/', views.add_dog , name='add_dog'),
    path('cart/', views.cart,name='cart'),
    path('add_to_cart/<int:dog_id>/',views.add_to_cart,name='add_to_cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]
