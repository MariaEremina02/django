from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from task_manager.views import upload_attachment, attachment_list, tags_list, ProjectListCreateAPIView, \
    ProjectDetailAPIView, AttachmentListCreateAPIView, AttachmentDetailAPIView, ProjectDetailsListCreateAPIView, \
    ProjectDetailsDetailAPIView, CommentDetailAPIView, CommentListCreateAPIView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from debug_toolbar.toolbar import debug_toolbar_urls

import rest_framework_simplejwt.views

urlpatterns = [
    path('', views.home, name='home'),
    path('tasks/', views.tasks_view),
    path('users/', views.users_view),
    path('upload/', views.upload_attachment, name='upload'),
    path('attachments/', views.attachment_list, name='attachments'),
    path('api/', include('api.urls')),
    path('schema/', SpectacularAPIView.as_view()),
    path('swagger/',SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('tags/', tags_list, name='tags-list'),
    path("projects/",ProjectListCreateAPIView.as_view()),
    path("projects/<int:pk>/",ProjectDetailAPIView.as_view()),
    path("comments/",CommentListCreateAPIView.as_view()),
    path("comments/<int:pk>/",CommentDetailAPIView.as_view()),
    path("attachments/",AttachmentListCreateAPIView.as_view()),
    path("attachments/<int:pk>/",AttachmentDetailAPIView.as_view()),
    path("project-details/",ProjectDetailsListCreateAPIView.as_view()),
    path("project-details/<int:pk>/",ProjectDetailsDetailAPIView.as_view()),
    path('protected-tasks/', views.protected_tasks, name='protected_tasks'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)