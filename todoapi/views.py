from django.shortcuts import render
from rest_framework import permissions, generics
from todo.models import Todo
from .serializers import Todocompletedserializer, Todocompleteserializer
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import  authenticate


# Create your views here.
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(username=data['username'], password=data['password'])
            token = Token.objects.create(user=user)
            user.save()
            return JsonResponse({'token': str(token)}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return JsonResponse({'error': 'please eneter different username'}, status=status.HTTP_406_NOT_ACCEPTABLE)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            return JsonResponse({'error': 'could not login'})
        else:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=status.HTTP_200_OK)


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
        return Todo.objects.filter(user=user)


class TodoCompleteView(generics.UpdateAPIView):
    serializer_class = Todocompleteserializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user, datecompleted__isnull=True)

    def perform_update(self, serializer):
        serializer.instance.datecompleted = timezone.now()
        serializer.save()
