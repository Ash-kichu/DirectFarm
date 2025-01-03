from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='Home'),
    path('shop/', views.shop, name='Shop'),
    path('about/', views.about, name='About'),
    path('farmers/', views.farmers, name='Farmers'),
    path('contact/', views.contact, name='Contact'),
    path('account/', views.account, name='Account'),
    path('account/orders/', views.orders, name='orders'),
    path('account/preferences/', views.preferences, name='preferences'),
    path('account/logout/', views.logout, name='logout'),
    path('cart/', views.cart, name='Cart'),
    path('signup/', views.signup, name='Sign Up'),
    path('login/', views.login, name='Login'),
]
