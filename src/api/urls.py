from django.urls import path

from .views import *

urlpatterns = [

    path(
        'tasks/get/',
        TaskGetAPIView.as_view()
    ),

    path(
        'tasks/post/',
        TaskPostAPIView.as_view()
    ),

    path(
        'tasks/put/',
        TaskPutAPIView.as_view()
    ),

    path(
        'tasks/delete/',
        TaskDeleteAPIView.as_view()
    ),
]