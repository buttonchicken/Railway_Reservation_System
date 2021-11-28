import features
from django.shortcuts import render
from django.template import loader
from features.models import Member
from .forms import UserLogin,UserReg
from django.contrib import auth
from django.contrib.auth import authenticate,login
from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request,'homepage.html')

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('/',request)
    else:
        return HttpResponse('<h1>Please Login First!!</h1>')   

#function for login
def log(request):
    if request.user.is_authenticated:
        a=request.user
        print(a)
        return HttpResponse('<h1><center>Already logged in, Please log out first!</center></h1>',request)
    else:
        template=loader.get_template('login.html')
        if request.method=='POST':
            form=UserLogin(request.POST)
            if form.is_valid():
                data=form.cleaned_data
                username=data['username']
                password=data['password']
                user=authenticate(username=username,password=password)
                if user is not None:
                    if user.is_active:
                        login(request,user)
                        return redirect('/',request)
                return HttpResponse('<h1>Invalid Credentials</h1>')
            return HttpResponse('<h1>invalid Data</h1>')
        else:
            return HttpResponse(template.render({}, request))

#function to register as a new user
def register(request):
    template = loader.get_template('register.html')
    if request.method=='POST':
        form=UserReg(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            data=form.cleaned_data
            usr=data['username']
            pas=data['password']
            eml=data['email']
            nmb=data['number']
            a=Member()
            a.username=usr
            a.password=pas
            a.email=eml
            a.number=nmb
            a.save()
            user.set_password(pas)
            user.save()
            user=authenticate(username=usr,password=pas)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return render(request,'homepage.html')
            return HttpResponse('<h1>VALID</h1>')
        return HttpResponse(template.render({'form':form},request))
    else:
        return HttpResponse(template.render({},request))