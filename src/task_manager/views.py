from django.http import HttpResponse
from django.db.models import Prefetch
from django.contrib.auth.models import User

from task_manager.models import Tasks

from django.shortcuts import get_object_or_404
from django.db.models import Count, Avg, Sum, F

from task_manager.models import Attachment
from task_manager.forms import AttachmentForm
from pathlib import Path
from django.core.files import File
from django.core.paginator import Paginator

from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView


from functools import lru_cache
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.http import JsonResponse


from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models.tags import Tags
from task_manager.v1.serializers.serializers import TagSerializer, AttachmentSerializer
from rest_framework import generics

from .models.projects import Projects
from task_manager.v1.serializers.serializers import ProjectSerializer
from .models.comments import Comments
from task_manager.v1.serializers.serializers import CommentSerializer
from .models.project_details import ProjectDetails
from task_manager.v1.serializers.serializers import ProjectDetailsSerializer


from django.contrib.auth.decorators import login_required, permission_required
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

#def home(request):
#    return render(request, 'tasks/home.html')
def home(request):
    return HttpResponse("Home page")

@login_required
def tasks_view(request):
    return render(request, 'tasks/tasks.html', {"tasks": tasks})

@permission_required('task_manager.view_tasks')
def protected_tasks(request):
    return HttpResponse("У вас есть право просмотра задач")

def users_view(request):
    return render(request, 'tasks/users.html', {"users": users})

#task + comments
def task_list(request):
    task = Tasks.objects.prefetch_related(
        Prefetch('comments', queryset=Comments.objects.select_related('user'))
    ).select_related('user', 'project')

    return render(request, 'tasks/task_list.html', {'tasks': tasks})

#конкретный пользователь
def user_tasks(request, user_id):
    user = User.objects.get(id=user_id)

    task = Tasks.objects.filter(user=user).prefetch_related(
        Prefetch(
            'comments',
            queryset=Comments.objects.filter(user=user)
        )
    )

    return render(request, 'tasks/user_tasks.html', {
        'tasks': tasks,
        'user': user
    })

from django.shortcuts import render, redirect
from .forms import TaskForm

def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks')
    else:
        form = TaskForm()

    return render(request, 'tasks/create_task.html', {'form': form})

#редактиров задачи
def edit_task(request, pk):
    task = get_object_or_404(Tasks, pk=pk)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks')
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/edit_task.html', {'form': form})


#запросы
def analytics(request):

    tasks_by_status = Tasks.objects.values('status').annotate(count=Count('id'))


    top_project = Tasks.objects.values('assignee__name') \
        .annotate(task_count=Count('id')) \
        .order_by('-task_count') \
        .first()


    tasks_with_comments = Tasks.objects.annotate(
        comment_count=Count('comments')
    )


    tasks_more_3_comments = Tasks.objects.annotate(
        comment_count=Count('comments')
    ).filter(comment_count__gt=3)


    avg_priority_by_project = Tasks.objects.values('assignee__name') \
        .annotate(avg_priority=Avg('priority'))


    from task_manager.models import Tags
    tags_priority_sum = Tags.objects.annotate(
        total_priority=Sum('tasks__priority')
    )


    tasks_comments_gt_tags = Tasks.objects.annotate(
        comment_count=Count('comments'),
        tag_count=Count('tags')
    ).filter(comment_count__gt=F('tag_count'))


    top_3_projects = Tasks.objects.values('assignee__name') \
        .annotate(comment_count=Count('comments')) \
        .order_by('-comment_count')[:3]


    avg_priority = Tasks.objects.aggregate(avg=Avg('priority'))['avg']

    complex_tasks = Tasks.objects.annotate(
        comment_count=Count('comments')
    ).filter(
        comment_count__gt=5,
        priority__gt=avg_priority
    )

    return render(request, 'tasks/analytics.html', {
        'tasks_by_status': tasks_by_status,
        'top_project': top_project,
        'tasks_with_comments': tasks_with_comments,
        'tasks_more_3_comments': tasks_more_3_comments,
        'avg_priority_by_project': avg_priority_by_project,
        'tags_priority_sum': tags_priority_sum,
        'tasks_comments_gt_tags': tasks_comments_gt_tags,
        'top_3_projects': top_3_projects,
        'complex_tasks': complex_tasks,
    })


# список файлов
def attachment_list(request):

    attachments = Attachment.objects.all().order_by('-id')

    # фильтр по title
    search = request.GET.get('search')

    if search:
        attachments = attachments.filter(title__icontains=search)

    paginator = Paginator(attachments, 3)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(request, 'attachments/list.html', {
        'page_obj': page_obj
    })


# загрузка файла
def upload_attachment(request):

    if request.method == 'POST':

        form = AttachmentForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = AttachmentForm()

    return render(request, 'attachments/upload.html', {
        'form': form
    })


# сохранение файла из внешнего пути
def save_external_file(request):

    path = Path('example.pdf')

    attachment = Attachment.objects.create(
        title='External file'
    )

    with path.open(mode='rb') as f:
        attachment.file = File(f, name=path.name)
        attachment.save()

    return redirect('/')


#представление
class HomePageView(TemplateView):
    template_name = "home.html"



class TaskListView(ListView):
    model = Tasks
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 5

class TaskDetailView(DetailView):
    model = Tasks
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

class ActiveTaskListView(ListView):
    model = Tasks
    template_name = 'tasks/active_tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Tasks.objects.filter(status='active')


#кэш
@lru_cache(maxsize=None)
def sum_positive(nums):
    if not nums:
        return 0

    first = nums[0]

    if first > 0:
        return first + sum_positive(nums[1:])
    else:
        return sum_positive(nums[1:])

print(sum_positive((1, -2, 3, 4, -5)))

@cache_page(60 * 30)
def my_view(request):
    data = {
        "message": "кэш вьюшки",
    }
    return JsonResponse(data)

def update_data(request):
    cache.clear()
    return JsonResponse({"status": "cache cleared"})


@api_view(["GET"])
def tags_list(request):
    tags = Tags.objects.all()

    serializer = TagSerializer(
        tags,
        many=True
    )

    return Response(serializer.data)

#список и создание
class ProjectListCreateAPIView(generics.ListCreateAPIView):

    queryset = Projects.objects.all()

    serializer_class = ProjectSerializer

#получение изменение удаление
class ProjectDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Projects.objects.all()

    serializer_class = ProjectSerializer


class AttachmentListCreateAPIView(
    generics.ListCreateAPIView):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer

class AttachmentDetailAPIView(
    generics.RetrieveUpdateDestroyAPIView):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer


class ProjectDetailsListCreateAPIView(
    generics.ListCreateAPIView):
    queryset = ProjectDetails.objects.all()
    serializer_class = ProjectDetailsSerializer

class ProjectDetailsDetailAPIView(
    generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectDetails.objects.all()
    serializer_class = ProjectDetailsSerializer



class CommentListCreateAPIView(
    generics.ListCreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer

class CommentDetailAPIView(
    generics.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
