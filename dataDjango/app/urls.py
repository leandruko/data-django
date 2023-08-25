from django.urls import path, include
from .views import home
from rest_framework import routers
from . import views



urlpatterns = [
    path('', home, name="home"),
    path('registro/', views.registro, name='registro'),
    path('login/', views.iniciar_sesion, name='login'),
    path('api/usuarios/', views.UserList.as_view(), name='user-list'),
]