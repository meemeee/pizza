from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # Add site authentication urls (for login, logout, password management)
    path('accounts/', include ('django.contrib.auth.urls')),
    # Add path for registration
    path('accounts/register/', views.register, name="register"),
    # Add path for Menu
    path('menu/', views.menu, name="menu"),
    # Path for placing an order
    path('menu/<str:item_id>', views.item),
    # Path for shopping cart
    path('cart', views.ItemListView.as_view(), name="cart"),
    # Path to view all orders
    path('orders', views.OrderListView.as_view(), name="orders"),
    # Path to view order's items
    path('order/<int:pk>', views.OrderDetailView.as_view(), name="order-detail"),
    # Path for placing an order
    path('new_order', views.submit_order, name="new_order"),
    # Path for changing order status
    path('order/<int:pk>/status', views.change_status_admin, name="change-order-status"),
    # Path for view all orders for admin
    path('orders/all', views.AllOrdersListView.as_view(), name="all-orders"),

]

