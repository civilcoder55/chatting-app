from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm


class Signin(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : "form-control form-control-lg",'autofocus': "None",'required':True,'placeholder':"Username",}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : "form-control form-control-lg",'required':True,'placeholder':"Password",}))




class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class' : "form-control form-control-lg",'autofocus': "None",'required':True,'placeholder':"Email",}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : "form-control form-control-lg",'autofocus': "None",'required':True,'placeholder':"Username",}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class' : "form-control form-control-lg",'required':True,'placeholder':"Password",}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class' : "form-control form-control-lg",'required':True,'placeholder':"Confirm Password",}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists() :
            raise forms.ValidationError("Email address is already exsist")
        else:
            return email



