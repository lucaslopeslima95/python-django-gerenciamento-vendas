from django.shortcuts import render
from django.shortcuts import render,redirect
from .forms import *
from .models import User
from django.contrib.auth import logout,login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import user_passes_test
from django.db.models import Q

def initial_page(request):
    return render(request,'dashboard.html')


def login_system(request):
    form = authForm()    
    try:
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
        #else:
         #   form = authForm()    
    except Exception as e :
        print(" Exceção ao tentar fazer o login{e}")
        
    return render(request, 'login.html', {'form': form})

@user_passes_test(lambda user: user.is_superuser,login_url='page_not_found')   
@login_required(login_url="login_system")
def save_user(request):
    try:
        form=None
        if request.method == "POST":
            form = registerUserForm(request.POST)
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
        else:
         form = registerUserForm()
    except Exception as e:
        print(e)
        messages.warning(request, "Ocorreu um erro ao registrar o usuário")
    return render(request, 'user/save_user.html', {'form': form})


def logout_system(request):
    logout(request)
    return redirect('user:initial_page')

@user_passes_test(lambda user: user.is_superuser,login_url='page_not_found')   
@login_required(login_url="login_system")
def erase_user(request, id):
    try:
        user = User.objects.get(id=id)
        user.delete()
    except Exception as e:
        print(e)
    return redirect('user:main_menu_user')

@user_passes_test(lambda user: user.is_superuser,login_url='page_not_found')   
@login_required(login_url="login_system")
def update_user(request,id):
    try:
        obj_user = User.objects.get(id=id)
        form = updateWithoutPasswordForm(request.POST or None, instance=obj_user)
        if request.method == "POST":
                obj_user = None
                if form.is_valid():
                        username = form.cleaned_data['username']
                        email = form.cleaned_data['email']
                        if not User.objects.filter(Q(username=username) & ~Q(id=id)).exists():
                            if not User.objects.filter(Q(email=email) & ~Q(id=id)).exists():
                                form.save()
                                messages.success(request, "Atualizado com sucesso")
                                return redirect('user:main_menu_user')
                            else:
                                messages.warning(request, "Email ja existe")    
                        else:
                            messages.warning(request, "Username ja existe")
    except User.DoesNotExist and Exception as e:
       print(f"Exceção no update user informations {e}")
       return redirect('user:main_menu_user')

    return render(request,'user/update_user.html',{'form':form})



@user_passes_test(lambda user: user.is_superuser,login_url='page_not_found')   
@login_required(login_url="login_system")
def update_user_password(request,id):
    form = updateUserPasswordForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            new_password = form.cleaned_data['password']
            User.objects.get(id=id).set_password(new_password)
            messages.success(request, "Atualizado com sucesso")
            return redirect('user:main_menu_user')
    return render(request,'user/update_user.html',{'form':form})

 
@user_passes_test(lambda user: user.is_superuser,login_url='page_not_found')   
@login_required(login_url="login_system")
def main_menu_user(request):
     return render(request,'user/main_menu_users.html',{'users':User.objects.all()})
 
 
def page_not_found(request):
   return render(request,'page_not_found.html')
     
     
     