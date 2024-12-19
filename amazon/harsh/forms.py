from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Customer
class Re_form(UserCreationForm):
    email=forms.EmailField()
    fields=['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].help_text=None
    
class Customer_form(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['Full_name','city','state','mobile']