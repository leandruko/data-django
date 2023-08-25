from django.shortcuts import render, redirect
from rest_framework import viewsets, generics
from .serializers import UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,'app/home.html')


def registro(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        
        if password == password_confirm:
            if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
                user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                messages.success(request, 'Usuario registrado exitosamente. Ahora puedes iniciar sesión.')
                return redirect('login')
            else:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'El nombre de usuario ya está registrado.')
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'El correo electrónico ya está registrado.')
        else:
            messages.error(request, 'Las contraseñas no coinciden.')
        
    return render(request, 'registration/registro.html')


def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Usuario autenticado con éxito, redirige a la página deseada (por ejemplo, la página de inicio).
            return redirect('home')
        else:
            messages.error(request, 'Credenciales incorrectas. Por favor, inténtalo de nuevo.')

    return render(request, 'registration/login.html')


#Generacion de la API

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
