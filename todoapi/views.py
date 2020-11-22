from django.shortcuts import render
from rest_framework import permissions, generics
from todo.models import Todo
from .serializers import Todocompletedserializer

# Create your views here.

class TodoListCompletedView(generics.ListAPIView):
    serializer_class = Todocompletedserializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user, datecompleted__isnull=False)

class TodoListCreateView(generics.ListCreateAPIView):
    serializer_class = Todocompletedserializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user, datecompleted__isnull=True)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class TodoListUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = Todocompletedserializer
    permission_classes = [permissions.IsAuthenticated, ]
    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user )
