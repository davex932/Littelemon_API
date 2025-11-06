from django.urls import path
from . import views

urlpatterns=[
    path('menu-items/', views.menu_items),
    path('menu-items/<int:pk>', views.item_detail),
    path('groups/manager/users/', views.managers),
    path('groups/delivery-crew/users/', views.deliverys),
    path('groups/delivery-crew/users/<int:pk>', views.delivery),
    path('groups/manager/users/<int:pk>', views.manager),
    path('cart/menu-items/', views.cart),
    path('orders/', views.orders),
    path('orders/<int:pk>', views.order_detail),
]