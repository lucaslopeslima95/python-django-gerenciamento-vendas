from django.shortcuts import render
from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import logout,login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def initial_page(request):
    return render(request,'dashboard.html')


def login_system(request):
    if request.user.is_authenticated:
        return initial_page(request)
    
    if request.method == "POST":
        form = authForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return initial_page(request)
            else:
                messages.warning(request, "Usuario ou Senha Errados.")
        else:
            messages.warning(request, "Credenciais inválidas.")
    else:
        form = authForm()    
    return render(request, 'login.html', {'form': form})


@login_required(login_url="login_system")
def save_user(request):
    if request.method == "POST":
        form = registerUserForm(request.POST)
        try:
            if form.is_valid():
                username = form.cleaned_data['username']
                if User.objects.filter(username=username).exists():
                    messages.warning(request, "Usuario já existe")
                else:
                    password = form.cleaned_data['password']
                    is_staff = form.cleaned_data['is_staff']
                    email = form.cleaned_data['email']
                    User.objects.create_user(username=username, password=password, email=email,is_staff=is_staff)
                    messages.success(request, "Salvo com sucesso")
                   
        except Exception as e:
            print(e)
            messages.warning(request, "Ocorreu um erro ao registrar o usuário")
    else:
        form = registerUserForm()
    return render(request, 'usuario/save_user.html', {'form': form})


def logout_system(request):
    logout(request)
    return redirect('login_system')

@login_required(login_url="login_system")
def erase_user(request, id):
    try:
        user = User.objects.get(id=id)
        user.delete()
    except Exception as e:
        print(e)
    return redirect('home')


@login_required(login_url="login_system")
def update_user(request,id):
    obj_user = None
    obj_user = User.objects.get(id=id)
    form = updateUserPasswordForm(request.POST or None, instance=obj_user)
    if request.method == "POST":
        if form.is_valid():
            form.save() 
            messages.success(request, "Atualizado com sucesso")
            return redirect('home')
    return render(request,'usuarios/update_user.html',{'form':form})
    
    
@login_required(login_url="login_system")
def main_menu_user(request):
     return render(request,'usuario/main_menu_users.html',{'users':User.objects.all()})