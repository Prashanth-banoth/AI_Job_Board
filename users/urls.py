from django.urls import path
from .views import home, register, login_view, dashboard, logout_view

urlpatterns = [
    path('', home),
    path('register/', register),
    path('login/', login_view),
    path('dashboard/', dashboard),
    path('logout/', logout_view),
]