from django.shortcuts import render

# ДАННЫЕ
tasks = [
    {"task_name": "Fix login bug", "status": "in progress", "priority": "high"},
    {"task_name": "Create navbar", "status": "done", "priority": "medium"},
    {"task_name": "Write tests", "status": "todo", "priority": "high"},
    {"task_name": "Update documentation", "status": "todo", "priority": "low"},
    {"task_name": "Deploy project", "status": "in progress", "priority": "medium"}
]

users = [
    {'name': 'Alice', 'age': 25, 'image': 'images/alice.jpg'},
    {'name': 'Bob', 'age': 30, 'image': 'images/bob.jpg'},
    {'name': 'Charlie', 'age': 28, 'image': 'images/charlie.jpg'},
    {'name': 'Diana', 'age': 22, 'image': 'images/diana.jpg'},
]

# вью

def home(request):
    return render(request, 'tasks/home.html')

def tasks_view(request):
    return render(request, 'tasks/tasks.html', {"tasks": tasks})

def users_view(request):
    return render(request, 'tasks/users.html', {"users": users})

