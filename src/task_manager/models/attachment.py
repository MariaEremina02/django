from django.db import models
from .task import Tasks


class Attachment(models.Model):

    task = models.ForeignKey(
        Tasks,
        on_delete=models.CASCADE,
        related_name='attachments'
    )

    title = models.CharField(max_length=255)

    file = models.FileField(
        upload_to='files/'
    )

    image = models.ImageField(
        upload_to='images/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title