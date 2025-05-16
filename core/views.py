from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def index(request):
    return render(request, 'core/index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('core:index')  # O redirige a donde prefieras después del login
        else:
            return render(request, 'core/login.html', {
                'error': 'Usuario o contraseña incorrectos'
            })
    
    return render(request, 'core/login.html')


def password_recovery(request):
    return render(request, 'core/password_recovery.html')