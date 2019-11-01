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
    path('menu/<str:item_id>', views.order),
]

