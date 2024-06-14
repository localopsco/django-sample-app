# todo/views.py

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from .models import Todo
from .forms import TodoForm, EC2InstanceForm
import boto3
from django.conf import settings
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

@csrf_exempt
def create_ec2_instance(request):
    if request.method == 'POST':
        form = EC2InstanceForm(request.POST)
        if form.is_valid():
            ec2_name = form.cleaned_data['name']
            subnet_id = form.cleaned_data['subnet_id']

            print("settings.AWS_REGION:", settings.AWS_REGION)
            print("settings.AWS_ACCESS_KEY_ID:", settings.AWS_ACCESS_KEY_ID)
            print("settings.AWS_SECRET_ACCESS_KEY:", settings.AWS_SECRET_ACCESS_KEY)

            try:
                # Initialize a session using Amazon EC2
                ec2_client = boto3.client(
                    'ec2',
                    region_name=settings.AWS_REGION,
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                )

                # Create an EC2 instance
                ec2_client.run_instances(
                    ImageId='ami-007020fd9c84e18c7',
                    InstanceType='t2.micro',
                    SubnetId=subnet_id,
                    MinCount=1,
                    MaxCount=1,
                    TagSpecifications=[
                        {
                            'ResourceType': 'instance',
                            'Tags': [
                                {'Key': 'Name', 'Value': ec2_name}
                            ]
                        }
                    ]
                )
                return render(request, 'todo/ec2_success.html')

            except Exception as e:
                return HttpResponse(f"An error occurred: {e}", status=500)

    else:
        form = EC2InstanceForm()

    return render(request, 'todo/ec2_form.html', {'form': form})
