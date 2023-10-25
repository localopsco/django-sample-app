from celery import shared_task
from .models import Todo

@shared_task
def mark_todo_completed(todo_id):
    todo = Todo.objects.get(pk=todo_id)
    todo.completed = True
    todo.save()
