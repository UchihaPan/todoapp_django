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
    success_url = reverse_lazy('current')
    template_name = 'todo/signup.html'

    def form_valid(self, form):
        view = super(Signup, self).form_valid(form)
        username, password = form.cleaned_data['username'], form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return view


@login_required
def create(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html')
    else:
        if request.method == 'POST':
            title = request.POST.get('title', '')
            memo = request.POST.get('memo', '')
            checkbox = request.POST.get('important', '')
            if checkbox != '':
                important = True
            else:
                important = False

            todo = Todo(title=title, memo=memo, important=important)
            todo.user = request.user
            todo.save()
            return redirect('current')

        return render(request, 'todo/createtodo.html',
                      {'error': 'please enter correct details.'})


@login_required
def current(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos': todos})


@login_required
def completed(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False)
    return render(request, 'todo/completedtodos.html', {'todos': todos})


@login_required
def view(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'GET':
        return render(request, 'todo/viewtodo.html', {'todo': todo})
    else:
        try:
            title = request.POST.get('title', '')
            memo = request.POST.get('memo', '')
            checkbox = request.POST.get('important', '')
            if checkbox != '':
                important = True
            else:
                important = False

            todo = Todo(title=title, description=memo, important=important)
            todo.user = request.user
            todo.save()
            return redirect('current')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'error': 'Bad info'})


@login_required
def complete(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('current')


@login_required
def delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('current')
