from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('shop/', views.shop_view, name='shop'),
    path('about/', views.about_view, name='about'),
    path('farmers/', views.farmers_view, name='farmers'),
    path('contact/', views.contact_view, name='contact'),
    path('account/', views.account_view, name='account'),
    path('account/orders/', views.orders_view, name='orders'),
    path('account/preferences/', views.preferences_view, name='preferences'),
    path('account/logout/', views.confirm_logout_view, name='confirm-logout'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.cart_view, name='checkout'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.home_view, name='forgot-password'),
    path('how-it-works/', views.how_it_works_view, name='how-it-works'),
]
