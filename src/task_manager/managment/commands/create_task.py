from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from task_manager.models import Tasks, Projects, Comments
from faker import Faker
import random

fake = Faker()

class Command(BaseCommand):
    help = 'Generate test data'

    def handle(self, *args, **kwargs):
        users = []
        for _ in range(100):
            user = User.objects.create_user(
                username=fake.user_name(),
                password='1234'
            )
            users.append(user)

        projects = []
        for _ in range(10):
            project = Projects.objects.create(name=fake.word())
            projects.append(project)

        tasks = []
        for _ in range(1000000):
            task = Tasks.objects.create(
                title=fake.word(),
                description=fake.text(),
                status=random.choice(['NEW', 'IN_PROGRESS', 'COMPLETED']),
                user=random.choice(users),
                project=random.choice(projects)
            )
            tasks.append(task)

        for task in tasks[:10000]:
            for _ in range(random.randint(1, 5)):
                Comments.objects.create(
                    task=task,
                    user=random.choice(users),
                    text=fake.sentence()
                )

        self.stdout.write(self.style.SUCCESS('Done!'))