from django.db import models
from django.conf import settings

from config.models import BaseModel



class Projects(BaseModel):
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

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#    owner = models.ForeignKey(
#        to="account.User",
#        related_name="projects",
#        on_delete=models.SET_NULL,
#        null=True,
#    )


    class Meta:
        ordering = ["-created_at"]
        db_table = "projects"
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return self.name