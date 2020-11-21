from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy


def home(request):
    return render(request, 'todo/home.html')


class Signup(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('currenttodos')
    template_name = 'todo/signup.html'

    def form_valid(self, form):
        view = super(Signup, self).form_valid(form)
        username, password = form.cleaned_data['username'], form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return view


@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html')
    else:
        if request.method == 'POST':
            title = request.POST.get('title', '')
            memo = request.POST.get('memo', '')
            checkbox = request.POST.get('important', '')
            if (checkbox != ''):
                important = True
            else:
                important = False

            todo = Todo(title=title, memo=memo, important=important)
            todo.user = request.user
            todo.save()
            return redirect('currenttodos')

        return render(request, 'todo/createtodo.html',
                      {'error': 'please enter correct details.'})


@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos': todos})


@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todo/completedtodos.html', {'todos': todos})


@login_required
def viewtodo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'GET':
        return render(request, 'todo/viewtodo.html', {'todo': todo})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'error': 'Bad info'})


@login_required
def completetodo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')


@login_required
def deletetodo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')
