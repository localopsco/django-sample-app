# todo/forms.py

from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'completed']

class EC2InstanceForm(forms.Form):
    name = forms.CharField(label='Instance Name', max_length=32)
    subnet_id = forms.CharField(label='Subnet ID', max_length=32)
