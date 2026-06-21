from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import TaskSerializer


class TaskGetAPIView(APIView):

    def get(self, request):
        tasks = [
            {
                "id": 1,
                "title": "Learn DRF",
                "description": "Study serializers"
            }
        ]

        serializer = TaskSerializer(tasks,many=True)
        return Response(serializer.data)

class TaskPostAPIView(APIView):

    def post(self, request):

        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.validated_data)

        return Response(serializer.errors)

class TaskPutAPIView(APIView):

    def put(self, request):
        task = {
            "title": "Old task",
            "description": "Old description"
        }

        serializer = TaskSerializer(task,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)


class TaskDeleteAPIView(APIView):
    def delete(self, request):

        return Response(
            {
                "message":
                "Task deleted"
            }
        )