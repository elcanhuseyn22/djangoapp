from django.shortcuts import render,redirect,HttpResponseRedirect
from .forms import RegisterForm,LoginForm
# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login,authenticate,logout as auth_logouth
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def userNotLogged(func):
    def _func(request, *args, **kwargs):     
        if request.user.is_authenticated:         
            return HttpResponseRedirect("/")
        return func(request, *args, **kwargs)
    return _func
    
@userNotLogged
def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        #----------
        name = form.cleaned_data.get('name')
        surname = form.cleaned_data.get('surname')
        email = form.cleaned_data.get('email')
        #----------
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        #----------
        newUser = User(username = username)
        newUser.set_password(password)

        newUser.save()

        auth_login(request,newUser)
        messages.success(request, 'Qeydiyyat prosesi uğurla tamamlandı!')

        return redirect("index")
    context = {
            "form":form
        }
    return render(request,"register.html",context)
@userNotLogged
def login(request):

    form = LoginForm(request.POST or None)

    context = {
        "form" : form
    }
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username = username,password = password)

        if user is None:
            messages.info(request,"İstifadəçi adı vəya parol düzgün deyil!")
            return render(request,"login.html",context)

        messages.success(request,"Giriş prosesi uğurla tamamlandı.")
        auth_login(request,user)
        return redirect("index")

    return render(request,"login.html",context)

def logout(request):
    auth_logouth(request)
    messages.success(request,"Çıxış prosesi uğurla sonlandırıldı.")
    return redirect("index")