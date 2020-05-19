from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from . import forms
from . models import profile_pic
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
import mimetypes
from pathlib import Path
from django.http import (FileResponse, Http404)
from django.utils.http import http_date
from django.utils._os import safe_join
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def log_in(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('messengerHome'))
    else:
        form = forms.Signin()
        if request.method == 'POST':
            form = forms.Signin(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username = username , password=password)
                if user:
                    if user.is_active :
                        login(request,user)
                        return HttpResponseRedirect(reverse('messengerHome'))
                else : 
                    messages.error(request, "Username or Password is incorrect")
                    return render(request , 'login.html' , {'signin' : form , 'title':'Login'})

        return render(request , 'login.html' , {'signin' : form , 'title':'Login'}) 



@login_required    
def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('messengerHome'))



def registe_r(request):
    if request.user.is_authenticated:
        onchange="this.form.submit()"
    else:
        form = forms.SignUpForm()
        if request.method == 'POST':
            form = forms.SignUpForm(request.POST)

            if form.is_valid():
                user = form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username = username , password=password)
                if user:
                    if user.is_active :
                        login(request,user)
                        return HttpResponseRedirect(reverse('messengerHome'))
            else:
                error = list(form.errors.as_data()[list(form.errors.as_data().keys())[0]][0])
                messages.error(request, error[0])
                return render(request , 'register.html' , {'signup' : form ,'title':'Register'})
            

        
        return render(request , 'register.html' , {'signup' : form ,'title':'Register'})


@login_required
def update(request):
    pic = request.FILES['pic']
    ob = profile_pic.objects.filter(user=request.user).first()
    ob.pic = pic
    ob.save()
    return HttpResponseRedirect(reverse('messengerHome'))












def media(request,path):
    if request.user.is_authenticated:
        fullpath = Path(safe_join(settings.MEDIA_ROOT, path))
        statobj = fullpath.stat()
        content_type, encoding = mimetypes.guess_type(str(fullpath))
        content_type = content_type or 'application/octet-stream'
        response = FileResponse(fullpath.open('rb'), content_type=content_type)
        response["Last-Modified"] = http_date(statobj.st_mtime)
        if encoding:
            response["Content-Encoding"] = encoding
        return response
    return HttpResponse(status=404)


