from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from config.models import BaseModel
from django.conf import settings
from ..managers import CompletedTaskManager

class TaskStatus(models.TextChoices):
    CREATED = "created"
    STARTED = "started"
    COMPLETED = "completed"
    CANCELED = "canceled"
    FAILED = "failed"

class Tasks(BaseModel):
    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name = "Наименование"
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание"
    )
    status = models.CharField(
        choices=TaskStatus,
        default=TaskStatus.CREATED,
        verbose_name="Статус"
    )
    priority = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        default=3,
        verbose_name="Приоритетность"
    )
    is_reopened = models.BooleanField(
        default=False,
        verbose_name = "Переоткрывалась ли"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="tasks"
    )
    assignee = models.ForeignKey(
        to = "Projects",
        related_name="tasks",
        on_delete=models.CASCADE,
        null = True,
        blank = True,
    )

    objects = models.Manager()
    completed = CompletedTaskManager()

    class Meta:
        ordering = ["-priority","-created_at"]
        db_table = "tasks"
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"