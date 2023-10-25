# todo/views.py

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from .models import Todo
from .forms import TodoForm
from .tasks import mark_todo_completed
from django.http import HttpResponse


def todo_list(request):
    todos = Todo.objects.all()
    return render(request, 'todo/todo_list.html', {'todos': todos})

def todo_detail(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    return render(request, 'todo/todo_detail.html', {'todo': todo})

def todo_create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save()
            return redirect('todo_detail', pk=todo.pk)
    else:
        form = TodoForm()
    return render(request, 'todo/todo_form.html', {'form': form})

def todo_update(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            todo = form.save()
            return redirect('todo_detail', pk=todo.pk)
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todo/todo_form.html', {'form': form})

def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        todo.delete()
        return redirect('todo_list')
    return render(request, 'todo/todo_confirm_delete.html', {'todo': todo})


@csrf_exempt
def todo_complete(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)

    if request.method == 'POST':
        mark_todo_completed(todo_id)

    return redirect('todo_list')
