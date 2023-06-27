from django.shortcuts import render
from django.shortcuts import render,redirect
from .forms import *
from .models import Collaborator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import user_passes_test
from django.db.models import Q
from User.models import User

@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')         
@login_required(login_url="login_system")
def main_menu_collaborator(request,name_to_filter=None):
    collaborators = None
    if not name_to_filter:
        collaborators = Collaborator.objects.all()
    else:
       collaborators =  Collaborator.objects.filter(name__startswith=name_to_filter)
    
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
    except Exception as e:
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
    except Exception as e:
        print(f"Exceção no deletar usuario {e}")
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
            
    except Collaborator.DoesNotExist and Exception as e:
       print(f"Exceção no update do colaborador {e}")
       messages.success(request, "Erro ao atualizar o colaborador")
       return redirect('collaborator:main_menu_collaborator')

    return render(request,'collaborator/update_collaborator.html',{'form':form})



@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')          
@login_required(login_url="login_system")
def update_collaborator_password(request,id):
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
    return render(request,'collaborator/update_collaborator.html',{'form':form})

@user_passes_test(lambda user: user.is_superuser,login_url='user:page_not_found')    
@login_required(login_url="login_system")
def update_active_collaborator(request,id):
    print(id)
    Collaborator.objects.filter(id=id).update(active = not Collaborator.objects.get(id=id).active)
    return redirect('collaborator:main_menu_collaborator')

@user_passes_test(lambda user: user.is_superuser,login_url='user:page_not_found')    
@login_required(login_url="login_system")
def main_menu_collaborator_with_filter(request):
    try:
        name = None
        if request.method == "POST":
            form = findByNameForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
    except Exception as e:
        print(f"Exceção ao pegar o valor para filtrar o Colaborador pelo Nome")
    return main_menu_collaborator(request,name)
    
     
     
     
