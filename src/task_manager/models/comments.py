from django.db import models
from django.conf import settings

from config.models import BaseModel

class Comments(BaseModel):
    message = models.CharField(
        max_length=255,
        unique=True,
        verbose_name = "Текст комментария"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
    )
    task = models.ForeignKey(
        to="task_manager.Tasks",
        related_name="comments",
        on_delete=models.CASCADE
    )


    class Meta:
        ordering = ["-created_at","message"]
        db_table = "comments"
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.message