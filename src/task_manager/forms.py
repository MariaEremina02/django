from django import forms
from django.forms import  Textarea
from django.core.validators import MinValueValidator,MaxValueValidator
from django.core.exceptions import ValidationError

from task_manager.models import Tasks, Attachment

#коммент
from django import forms

class CommentForm(forms.Form):
    message = forms.CharField(
        label="Текст комментария",
        widget=forms.Textarea
    )
    user = forms.CharField(
        label="Ваше имя",
        max_length=100
    )

class CommentsForm(forms.Form):
    message = forms.CharField(
        label="Текст комментария",
        widget=forms.Textarea
    )
    user = forms.CharField(
        label="Ваше имя",
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

from .models import Tasks

class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['name', 'description', 'priority', 'status']


#validation custom
class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['name', 'description', 'priority', 'status']

    def clean(self):
        cleaned_data = super().clean()
        priority = cleaned_data.get("priority")
        description = cleaned_data.get("description")

        if priority == "high" and not description:
            raise forms.ValidationError(
                "Нельзя ставить высокий приоритет без описания!"
            )

#custom виджеты
class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['name', 'description', 'priority', 'status']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 6,
                'cols': 60,
                'class': 'form-control'
            })
        }


class AttachmentForm(forms.ModelForm):

    class Meta:
        model = Attachment
        fields = ['task', 'title', 'file', 'image']

    def clean_file(self):

        file = self.cleaned_data.get('file')

        if file.size > 5 * 1024 * 1024:
            raise forms.ValidationError(
                'Файл больше 5MB'
            )

        return file