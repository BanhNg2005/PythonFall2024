from django.shortcuts import render, redirect
import requests
from django.contrib import messages
from django.conf import settings


# Create your views here.

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        response = requests.post(
            f"{settings.FLASK_API_URL}/v0/users/login",
            json={'email': email, 'password': password}
        )
        data = response.json()
        
        if 'token' in data:
            request.session['token'] = data['token']
            request.session['user'] = data['logged_user']
            return redirect('dashboard') # This will be created in the next step
        else:
            messages.error(request, data.get('error', 'Login failed'))
            
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'GET':
        # Clear any existing messages when loading the page
        storage = messages.get_messages(request)
        storage.used = True
        return render(request, 'signup.html')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        
        # Check for empty fields
        if not all([name, email, password]):
            messages.error(request, 'Something wrong happened when creating user!')
            return render(request, 'signup.html')
            
        response = requests.post(
            f"{settings.FLASK_API_URL}/v0/users/signup",
            json={'name': name, 'email': email, 'password': password}
        )
        data = response.json()
        
        if 'id' in data:
            return redirect('login')
        else:
            messages.error(request, data.get('error', 'Something wrong happened when creating user!'))
            return render(request, 'signup.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')