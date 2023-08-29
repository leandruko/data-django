from django.shortcuts import render, redirect
from rest_framework import viewsets, generics
from .serializers import UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail

'''
from django.views.decorators.csrf import requires_csrf_token
from django.template import loader
from django.http import HttpResponseNotFound
'''

# Create your views here.
def home(request):
    return render(request,'app/home.html')


from django.contrib.auth.models import User
from django.contrib.auth import login
from django.core.mail import send_mail
from django.contrib import messages

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
                # Crea el usuario
                user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                
                # Envío de correo electrónico al usuario registrado
                subject = 'Registro Exitoso'
                message = '¡Gracias por registrarte en nuestra aplicación!'
                from_email = 'noreply@tudominio.com'
                recipient_list = [email]
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                
                # Iniciar sesión al usuario después del registro
                login(request, user)
                
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
            
            # Mostrar mensaje de éxito
            messages.success(request, 'Has iniciado sesión correctamente.')
            
            return redirect('home')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
            
    return render(request, 'registration/login.html')

def recuperar_contrasenia(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            
            # Generar token para restablecer la contraseña
            token_generator = PasswordResetTokenGenerator()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            
            # Construir el enlace para restablecer la contraseña
            reset_link = request.build_absolute_uri(f'/reset-contrasenia/{uid}/{token}/')
            
            # Enviar correo electrónico con el enlace
            send_mail(
                'Recuperación de Contraseña',
                f'Para restablecer tu contraseña, haz clic en el siguiente enlace: {reset_link}',
                'noreply@tudominio.com',
                [email],
                fail_silently=False,
            )
            
            messages.success(request, 'Se ha enviado un enlace de recuperación a tu correo electrónico.')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'No se encontró ningún usuario con ese correo electrónico.')
            
    return render(request, 'registration/recuperar_contrasenia.html')



def restablecer_contrasenia(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
        token_generator = PasswordResetTokenGenerator()
        if token_generator.check_token(user, token):
            if request.method == 'POST':
                new_password = request.POST['new_password']
                user.set_password(new_password)
                user.save()
                
                messages.success(request, 'Tu contraseña ha sido restablecida correctamente. Ahora puedes iniciar sesión con tu nueva contraseña.')
                return redirect('login')
                
            return render(request, 'registration/restablecer_contrasenia.html', {'uidb64': uidb64, 'token': token})
    except User.DoesNotExist:
        pass
    
    messages.error(request, 'El enlace de restablecimiento de contraseña no es válido.')
    return redirect('login')



'''
@requires_csrf_token
def pagina_no_encontrada(request, exception):
    template = loader.get_template('404.html')
    return HttpResponseNotFound(template.render())
'''




#Generacion de la API

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
