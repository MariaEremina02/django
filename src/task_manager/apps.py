from django.apps import AppConfig


class TaskManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task_manager'
    verbose_name = "Менеджер задач"

def ready(self):
    # Implicitly connect signal handlers decorated with @receiver.
    from task_manager.signals import create_comment

    # # Explicitly connect a signal handler.
    # post_save.connect(my_test_signal)