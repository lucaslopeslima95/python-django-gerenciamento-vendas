from django.shortcuts import render
from django.shortcuts import render,redirect
from .forms import *
from .models import Collaborator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import user_passes_test
from User.models import User
from sqlite3 import IntegrityError

@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')         
@login_required(login_url="login_system")
def main_menu_collaborator(request):
    try:
        name_to_filter = request.session['filter']
        collaborators = None
        if not name_to_filter:
            collaborators = Collaborator.objects.filter(user__is_deleted=True)
            request.session['filter'] = None
        else:
            collaborators =  Collaborator.objects.filter(name__startswith=name_to_filter,user__is_deleted=True)
            request.session['filter'] = None
    except (Exception,IntegrityError) as e:
        print(f"Exceção ao listar usuarios - {e}")
    return render(request,'collaborator/main_menu_collaborator.html',{'collaborators':collaborators,'findByNameForm': findByNameForm})

@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')        
@login_required(login_url="login_system")
def save_collaborator(request):
    try:
        if request.method == "POST":
            form = registerCollaboratorForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                cpf = form.cleaned_data['cpf']
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                password_check = form.cleaned_data['password_check']
                cpf = cpf.replace(".", "").replace(".", "").replace("-", "")
                if password != password_check:
                    messages.success(request, "As senha não coincidem")
                else:
                    user = User.objects.create(username=username, password=password, email=email)
                    Collaborator.objects.create(name=name,cpf=cpf, user=user)
                    user.set_password(password)
                    user.save()
                    messages.success(request, "Salvo com sucesso")
                    return redirect('collaborator:main_menu_collaborator')
                    
        else:
            form = registerCollaboratorForm()
    except (Exception,IntegrityError) as e:
        if 'username' in str(e):
            messages.error(request, "O nome de usuário já existe")
        elif 'cpf' in str(e):
            messages.error(request, "O CPF já está registrado")
        elif 'email' in str(e):
            messages.error(request, "O email já está registrado")
        else:
            print(f"Exceção ao salvar um colaborador - {e}")
            messages.warning(request, "Ocorreu um erro ao registrar o Colaborador")
    return render(request, 'collaborator/save_collaborator.html', {'form': form})

@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')          
@login_required(login_url="login_system")
def erase_collaborator(request, id):
    try:
        collaborator = Collaborator.objects.get(id=id)
        User.objects.get(id = collaborator.user.id).delete()
        collaborator.delete() 
    except (Exception,User.DoesNotExist,Collaborator.DoesNotExist) as e:
        print(f"Exceção no excluir usuario {e}")
    return redirect('collaborator:main_menu_collaborator')

@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')          
@login_required(login_url="login_system")
def update_collaborator(request,id):
    try:
        collaborator_selected = Collaborator.objects.get(id=id)
        form = updateWithoutPasswordForm(request.POST or None, instance=collaborator_selected)
        if request.method == "POST":
            if form.is_valid():
                cpf = form.cleaned_data['cpf']
                cpf = cpf.replace(".", "").replace(".", "").replace("-", "")
                collaborator_selected.cpf = cpf
                collaborator_selected.user.email = form.cleaned_data['email']
                collaborator_selected.user.username = form.cleaned_data['username']
                collaborator_selected.user.save()
                collaborator_selected.save()
                messages.success(request, "Atualizado com sucesso")
                return redirect('collaborator:main_menu_collaborator')
            else:
                messages.warning(request, "Dados Invalido")
        else:
            form.initial['email'] = collaborator_selected.user.email
            form.initial['username'] = collaborator_selected.user.username
     
    except (Exception,IntegrityError,Collaborator.DoesNotExist) as e:
        if 'username' in str(e):
            messages.error(request, "O nome de usuário já existe")
        elif 'cpf' in str(e):
            messages.error(request, "O CPF já está registrado")
        elif 'email' in str(e):
            messages.error(request, "O email já está registrado")
        else:
            print(f"Exceção no update do colaborador - {e}")
            messages.success(request, "Erro ao atualizar o colaborador")
    return render(request,'collaborator/update_collaborator.html',{'form':form,'collaborator':collaborator_selected})



@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')          
@login_required(login_url="login_system")
def update_collaborator_password(request,id):
    try:
        if request.method == "POST":
            form = updateUserPasswordForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['password']
                new_password_check = form.cleaned_data['password_check']
                if new_password == new_password_check:
                    collaborator = Collaborator.objects.get(id=id)
                    user = User.objects.get(id = collaborator.user)
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, "Atualizado com sucesso")
                    return redirect('collaborator:main_menu_collaborator')
            else:
                messages.warning(request, "Dados Invalido")
        else:
            form = updateUserPasswordForm()  
    except Exception as e:
        print(f"Exceção aconteceu ao Atualizar a senha de um colaborador {e}")
    return render(request,'collaborator/update_collaborator.html',{'form':form})

@user_passes_test(lambda user: user.is_superuser,login_url='user:page_not_found')    
@login_required(login_url="login_system")
def update_active_collaborator(request,id):
    try:
        Collaborator.objects.filter(id=id).update(active = not Collaborator.objects.get(id=id).active)
    except Exception as e:
        print(f"Exceção ao atualizar a situação do colaborador{e}")
    return redirect('collaborator:update_collaborator')


@user_passes_test(lambda user: user.is_superuser,login_url='user:page_not_found')    
@login_required(login_url="login_system")
def main_menu_collaborator_with_filter(request):
    try:
        if request.method == "POST":
            form = findByNameForm(request.POST)
            if form.is_valid():
                request.session['filter'] = form.cleaned_data['name']
    except Exception as e:
        print(f"Exceção ao pegar o valor para filtrar o Colaborador pelo Nome - {e}")
        
    return redirect('collaborator:main_menu_collaborator')
    
     
     
     
