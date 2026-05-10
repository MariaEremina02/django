from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from task_manager.views import upload_attachment, attachment_list

urlpatterns = [
    path('', views.home, name='home'),
    path('tasks/', views.tasks_view),
    path('users/', views.users_view),
    path('upload/', views.upload_attachment, name='upload'),
    path('attachments/', views.attachment_list, name='attachments'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)