from rest_framework import serializers

from task_manager.models.task import Tasks
from task_manager.models.tags import Tags
from task_manager.models.projects import Projects
from task_manager.models.project_details import ProjectDetails
from task_manager.models.attachment import Attachment
from task_manager.models.comments import Comments


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        instance["title"] = validated_data.get("title",instance["title"])
        instance["description"] = validated_data.get("description",instance["description"])
        return instance


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        instance["username"] = validated_data.get("username",instance["username"])
        instance["email"] = validated_data.get("email",instance["email"])
        return instance



class TaskModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = [
            "id",
            "name",
            "description",
            "status",
            "priority",
            "is_reopened",
            "created_at",
            "updated_at",
            "users",
            "assignee"
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = [
            "id",
            "name",
            "tasks"
        ]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = [
            "id",
            "name",
            "description",
            "owner"
        ]


class ProjectDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDetails
        fields = [
            "id",
            "info",
            "serial_id",
            "project"
        ]


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = [
            "id",
            "task",
            "title",
            "file",
            "image",
            "created_at"
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = [
            "id",
            "message",
            "user",
            "task"
        ]