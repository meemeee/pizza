from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.index, name="index")
]

# Add site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include ('django.contrib.auth.urls'))
]

# Add path for registration
urlpatterns += [
    path('accounts/register/', views.register, name="register")
]

# Add path for Menu

urlpatterns += [
    path('menu/', views.menu, name="menu")
]