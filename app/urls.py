from django.conf.urls import handler404
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('shop/', views.shop_view, name='shop'),
    path('shop/farmer/<int:farmer_id>/', views.shop_view_by_farmer, name='shop_by_farmer'),
    path('shop/category/<str:category>/', views.shop_view_by_category, name='shop_by_category'),
    path('about/', views.about_view, name='about'),
    path('farmers/', views.farmers_view, name='farmers'),
    path('contact/', views.contact_view, name='contact'),
    path('account/', views.account_view, name='account'),
    path('account/orders/', views.orders_view, name='orders'),
    path('account/logout/', views.confirm_logout_view, name='confirm-logout'),
    path('account/products/', views.products_view, name='products'),
    path('account/cart/', views.cart_view, name='cart'),
    path('checkout/', views.cart_view, name='checkout'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password_view, name='forgot-password'),
    path('how-it-works/', views.how_it_works_view, name='how-it-works'),
    path('update-profile/', views.update_profile_view, name='update_profile'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('product/<int:product_id>/', views.product_detail_view, name='product_detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart_view, name='remove_from_cart'),
]

handler404 = 'app.views.custom_404'
