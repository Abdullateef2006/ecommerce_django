from django.urls import path, re_path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', product_list, name='list'),
    path('wishlist', wishlist_list, name='wishlist'),
    path('wishlist/<str:pk>', wishlist, name='wishlist'),
    path('search/', search, name='search'),
    path('clear_cart/', clear_cart, name='clear_cart'),
    path('clear_wishlist/', clear_wishlist, name='clear_wishlist'),

    path('cart_list', cart_list, name='cart_list'),
    path('remove_wishlist/<int:id>', remove_wishlist, name='remove_wishlist'),

    path('remove_cart/<int:id>', remove_cart, name='remove_cart'),
    path('add_cart/<int:id>', add_cart, name='add_cart'),
    path('profile', profile, name='profile'),
    path('list/<str:pk>', list_category, name='list_category'),
    path('list/details/<str:pk>', list_details, name='details'),
    path('initiate-payment', initiate_payment, name="initiate_payment"),
    path('signup/', register, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('send_email_notification/', send_purchase_notification_email,
         name='send_purchase_notification'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
