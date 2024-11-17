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
            return redirect('home') # This will be created in the next step
        else:
            messages.error(request, data.get('error', 'Login failed'))
            
    return render(request, 'authentication/login.html')

def signup_view(request):
    if request.method == 'GET':
        # Clear any existing messages when loading the page
        storage = messages.get_messages(request)
        storage.used = True
        return render(request, 'authentication/signup.html')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        
        # Check for empty fields
        if not all([name, email, password]):
            messages.error(request, 'Something wrong happened when creating user!')
            return render(request, 'authentication/signup.html')
            
        response = requests.post(
            f"{settings.FLASK_API_URL}/v0/users/signup",
            json={'name': name, 'email': email, 'password': password}
        )
        data = response.json()
        
        if 'id' in data:
            return redirect('login')
        else:
            messages.error(request, data.get('error', 'Something wrong happened when creating user!'))
            return render(request, 'authentication/signup.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')

def home_view(request):
    if not request.session.get('token'):
        return redirect('login')
    return render(request, 'task/home.html')

def create_task_view(request):
    if not request.session.get('token'):
        return redirect('login')

    token = request.session.get('token')
    headers = {'x-access-token': token}

    # Fetch all users for the assignment dropdown
    users_response = requests.get(
        f"{settings.FLASK_API_URL}/v0/users/all",
        headers=headers
    )
    users = users_response.json().get('users', [])

    if request.method == 'POST':
        # Handle task creation
        title = request.POST.get('title')
        description = request.POST.get('description')
        assignee_uid = request.POST.get('assignee_uid')

        task_data = {
            'description': description,
            'assignedToUid': assignee_uid,
        }

        response = requests.post(
            f"{settings.FLASK_API_URL}/tasks",
            headers=headers,
            json=task_data
        )

        if response.status_code == 201:
            messages.success(request, 'Task created successfully.')
            return redirect('view_task_created')
        else:
            messages.error(request, 'Failed to create task.')

    context = {
        'users': users,
    }
    return render(request, 'task/create_task.html', context)

def view_task_assigned_view(request):
    if not request.session.get('token'):
        return redirect('login')

    token = request.session.get('token')
    headers = {'x-access-token': token}

    # Fetch tasks assigned to the current user
    assigned_tasks_response = requests.get(
        f"{settings.FLASK_API_URL}/tasks/assignedto",
        headers=headers
    )
    assigned_tasks = assigned_tasks_response.json().get('tasks', [])

    context = {
        'assigned_tasks': assigned_tasks,
    }
    return render(request, 'task/view_task_assigned.html', context)

def view_task_created_view(request):
    if not request.session.get('token'):
        return redirect('login')

    token = request.session.get('token')
    headers = {'x-access-token': token}

    # Fetch tasks created by the current user
    created_tasks_response = requests.get(
        f"{settings.FLASK_API_URL}/tasks/createdby",
        headers=headers
    )
    created_tasks = created_tasks_response.json().get('tasks', [])

    context = {
        'created_tasks': created_tasks,
    }
    return render(request, 'task/view_task_created.html', context)