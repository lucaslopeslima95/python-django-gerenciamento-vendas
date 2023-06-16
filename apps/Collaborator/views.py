from django.shortcuts import render
from django.shortcuts import render,redirect
from .forms import *
from .models import Collaborator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import user_passes_test
from django.db.models import Q

def initial_page(request):
    return render(request,'dashboard.html')

@user_passes_test(lambda user: user.is_staff or user.is_superuser ,login_url='page_not_found')    
@login_required(login_url="login_system")
def save_collaborator(request):
    try:
        form=None
        if request.method == "POST":
            form = registerCollaboratorForm(request.POST)
            if form.is_valid():
                form.save()      
                messages.success(request, "Salvo com sucesso")
        else:
         form = registerCollaboratorForm()
    except Exception as e:
        print(e)
        messages.warning(request, "Ocorreu um erro ao registrar o Colaborador")
    return render(request, 'collaborator/save_collaborator.html', {'form': form})

@user_passes_test(lambda user: user.is_staff or user.is_superuser ,login_url='page_not_found')      
@login_required(login_url="login_system")
def erase_user(request, id):
    try:
        obj_collaborator = Collaborator.objects.get(id=id)
        obj_collaborator.delete()
    except Exception as e:
        print(e)
    return redirect('main_menu_collaborator')

@user_passes_test(lambda user: user.is_staff or user.is_superuser ,login_url='page_not_found')      
@login_required(login_url="login_system")
def update_user(request,id):
    try:
        obj_collaborator = Collaborator.objects.get(id=id)
        form = updateWithoutPasswordForm(request.POST or None, instance=obj_user)
        if request.method == "POST":
                obj_user = None
                if form.is_valid():
                        username = form.cleaned_data['username']
                        email = form.cleaned_data['email']
                        if not Collaborator.objects.filter(Q(username=username) & ~Q(id=id)).exists():
                            if not Collaborator.objects.filter(Q(email=email) & ~Q(id=id)).exists():
                                form.save()
                                messages.success(request, "Atualizado com sucesso")
                                return redirect('main_menu_user')
                            else:
                                messages.warning(request, "Email ja existe")    
                        else:
                            messages.warning(request, "Username ja existe")
    except Collaborator.DoesNotExist and Exception as e:
       print(f"Exceção no update do colaborador {e}")
       return redirect('main_menu_user')

    return render(request,'collaborator/update_collaborator.html',{'form':form})



@user_passes_test(lambda user: user.is_staff or user.is_superuser ,login_url='page_not_found')      
@login_required(login_url="login_system")
def update_user_password(request,id):
    form = updateUserPasswordForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            new_password = form.cleaned_data['password']
            Collaborator.objects.get(id=id).set_password(new_password)
            print('2')
            messages.success(request, "Atualizado com sucesso")
            print('3')
            return redirect('main_menu_user')
    return render(request,'user/update_user.html',{'form':form})

 
@user_passes_test(lambda user: user.is_staff or user.is_superuser ,login_url='page_not_found')      
@login_required(login_url="login_system")
def main_menu_user(request):
     return render(request,'user/main_menu_users.html',{'users':Collaborator.objects.all()})
 

     
     
     
