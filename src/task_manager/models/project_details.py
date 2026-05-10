from django.db import models


from config.models import BaseModel



class ProjectDetails(BaseModel):
    info = models.CharField(
        max_length=64,
        unique=True,
        verbose_name = "Информация"
    )
    serial_id = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="ID проекта"
    )

    project = models.OneToOneField(
        to="Projects",
        related_name="project_detail",
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        ordering = ["-created_at"]
        db_table = "project_details"
        verbose_name = "Детали проекта"
        verbose_name_plural = "Детали проектов"

    def __str__(self):
        return self.info