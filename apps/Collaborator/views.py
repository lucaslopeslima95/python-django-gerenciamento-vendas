from django.shortcuts import render
from django.shortcuts import render,redirect
from .forms import *
from .models import Collaborator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import user_passes_test
from django.db.models import Q

@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')         
@login_required(login_url="login_system")
def main_menu_collaborator(request):
     return render(request,'collaborator/main_menu_collaborator.html',{'collaborators':Collaborator.objects.all()})

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
                if password != password_check:
                    messages.success(request, "As senha não coincidem")
                else:
                    Collaborator.objects.create(username=username,name=name, password=password,email=email,cpf=cpf,active=True)
                    messages.success(request, "Salvo com sucesso")
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
        Collaborator.objects.get(id=id).delete()
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
                        cpf.replace(".","").replace(".","").replace("-","")
                        username = form.cleaned_data['username']
                        email = form.cleaned_data['email']
                        #cpf = form.cleaned_data['cpf']
                         
                        if not Collaborator.objects.filter(Q(username=username) & ~Q(id=id)).exists():
                            if not Collaborator.objects.filter(Q(email=email) & ~Q(id=id)).exists():
                                if not Collaborator.objects.filter(Q(cpf=cpf) & ~Q(id=id)).exists():
                                    form.save()
                                    messages.success(request, "Atualizado com sucesso")
                                    return redirect('collaborator:main_menu_collaborator')
                                else:
                                    messages.warning(request, "Cpf ja existe")    
                            else:
                                messages.warning(request, "Email ja existe")
                        else:
                            messages.warning(request, "Cpf ja existe")
                else:
                    messages.warning(request, "Dados Invalido")
            
    except Collaborator.DoesNotExist and Exception as e:
       print(f"Exceção no update do colaborador {e}")
       return redirect('collaborator:main_menu_collaborator')

    return render(request,'collaborator/update_collaborator.html',{'form':form})



@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')          
@login_required(login_url="login_system")
def update_collaborator_password(request,id):
    if request.method == "POST":
        form = updateUserPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['password']
            Collaborator.objects.get(id=id).set_password(new_password)
            messages.success(request, "Atualizado com sucesso")
            return redirect('collaborator:main_menu_collaborator')
        else:
            messages.warning(request, "Dados Invalido")
    else:
        form = updateUserPasswordForm()  
    return render(request,'collaborator/update_collaborator.html',{'form':form})

 

 

     
     
     
