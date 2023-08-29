from django.urls import path, include
from .views import home
from rest_framework import routers
from . import views

# handler404 = 'app.views.pagina_no_encontrada'


urlpatterns = [
    path('', home, name="home"),
    path('registro/', views.registro, name='registro'),
    path('login/', views.iniciar_sesion, name='login'),
    path('api/usuarios/', views.UserList.as_view(), name='user-list'),
    path('recuperar-contrasenia/', views.recuperar_contrasenia, name='recuperar-contrasenia'),
    path('reset-contrasenia/<str:uidb64>/<str:token>/', views.restablecer_contrasenia, name='restablecer-contrasenia'),

]