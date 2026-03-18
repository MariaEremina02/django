
from django.urls import path
from src.task_manager.views import index

urlpatterns = [
    path('index/', index),
]