import hashlib
from sqlite3 import IntegrityError

from django.contrib import messages
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from User.models import User
from validate_docbr import CPF

from .forms import (registerCollaboratorForm, updateUserPasswordForm,
                    updateWithoutPasswordForm)
from .models import Collaborator


@user_passes_test(lambda user: user.is_superuser or user.is_staff,
                  login_url='user:page_not_found')
@login_required(login_url="login_system")
def main_menu_collaborator(request):
    try:
        filter = None
        collaborators = None
        if 'filter' in request.session:
            filter = request.session['filter']
        else:
            filter = None
        if not filter:
            collaborators = Collaborator.objects.filter(user__is_deleted=True)
            request.session['filter'] = None
        else:
            collaborators = Collaborator.objects.filter(
                name__startswith=filter, user__is_deleted=True)
            request.session['filter'] = None
    except (Exception, IntegrityError) as e:
        print(f"Exceção ao listar usuarios - {e}")
    return render(request, 'collaborator/main_menu_collaborator.html',
                  {'collaborators': collaborators})

def generate_md5(text):
    md5_hash = hashlib.md5()
    md5_hash.update(text.encode('utf-8'))
    md5_hex = md5_hash.hexdigest()
    return md5_hex

@user_passes_test(lambda user: user.is_superuser or user.is_staff,
                  login_url='user:page_not_found')
@login_required(login_url="login_system")
def save_collaborator(request):
    try:
        if request.method == "POST":
            form = registerCollaboratorForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                cpf_mask = form.cleaned_data['cpf']
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                password_check = form.cleaned_data['password_check']
                cpf = cpf_mask.replace(".", "").replace(".", "").replace("-", "")
                md5 = generate_md5(cpf_mask)
                if password != password_check:
                    messages.success(request, "As senha não coincidem")
                    return redirect('collaborator:save_collaborator')
                else:
                    validation = CPF()
                    if not Collaborator.objects.filter(cpf=cpf).exists() and validation.validate(cpf_mask):
                        user = User.objects.create(
                            username=username, password=password, email=email)
                        Collaborator.objects.create(
                            name=name, cpf=cpf, user=user,cod_auth=md5)
                        user.set_password(password)
                        user.save()
                        messages.success(request, "Salvo com sucesso")
                        return redirect('collaborator:main_menu_collaborator')
                    else:
                        messages.warning(request, "O CPF Inválido")
                        return render(request, 'user/save_user.html', {'form': form})
        else:
            form = registerCollaboratorForm()
    except (Exception, IntegrityError) as e:
        if 'email' in str(e):
            messages.warning(request, "O email já está registrado")
        elif 'username' in str(e):
            messages.warning(request, "O nome de usuário já existe")
        else:
            print(f"Exceção ao salvar um colaborador - {e}")
            messages.warning(request, "O CPF já está registrado")

    return render(request,
                  'collaborator/save_collaborator.html', {'form': form})


@user_passes_test(lambda user: user.is_superuser or user.is_staff,
                  login_url='user:page_not_found')
@login_required(login_url="login_system")
def erase_collaborator(request, id):
    try:
        collaborator = Collaborator.objects.get(id=id)
        User.objects.get(id=collaborator.user.id).delete()
        collaborator.delete()
    except (Exception, User.DoesNotExist, Collaborator.DoesNotExist) as e:
        print(f"Exceção no excluir usuario {e}")
    return redirect('collaborator:main_menu_collaborator')


@user_passes_test(lambda user: user.is_superuser or user.is_staff,
                  login_url='user:page_not_found')
@login_required(login_url="login_system")
def update_collaborator(request, id):
    try:
        collaborator_selected = Collaborator.objects.get(id=id)
        form = updateWithoutPasswordForm(request.POST or None,
                                         instance=collaborator_selected)
        if request.method == "POST":
            if form.is_valid():
                cpf_mask = form.cleaned_data['cpf']
                cpf = cpf_mask.replace(".", "").replace(".", "").replace("-", "")
                
                collaborator_selected.cpf = cpf
                collaborator_selected.user.email = form.cleaned_data['email']
                collaborator_selected.user.username = form\
                    .cleaned_data['username']
                collaborator_selected.user.save()
                collaborator_selected.save()
                messages.success(request, "Atualizado com sucesso")
                return redirect('collaborator:main_menu_collaborator')
            else:
                messages.warning(request, "Dados Invalido")
        else:
            form.initial['email'] = collaborator_selected.user.email
            form.initial['username'] = collaborator_selected.user.username
    except (Exception, IntegrityError, Collaborator.DoesNotExist) as e:
        if 'username' in str(e):
            messages.warning(request, "O nome de usuário já existe")
        elif 'cpf' in str(e):
            messages.warning(request, "O CPF já está registrado")
        elif 'email' in str(e):
            messages.warning(request, "O email já está registrado")
        else:
            print(f"Exceção no update do colaborador - {e}")
            messages.success(request, "Erro ao atualizar o colaborador")
    return render(request,
                  'collaborator/update_collaborator.html',
                  {'form': form, 'collaborator': collaborator_selected})


@user_passes_test(lambda user: user.is_superuser or user.is_staff,
                  login_url='user:page_not_found')
@login_required(login_url="login_system")
def update_collaborator_password(request, id):
    try:
        if request.method == "POST":
            form = updateUserPasswordForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['password']
                new_password_check = form.cleaned_data['password_check']
                if new_password == new_password_check:
                    collaborator = Collaborator.objects.get(id=id)
                    user = User.objects.get(id=collaborator.user.pk)
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
    return render(request,
                  'collaborator/update_collaborator_password.html',
                  {'form': form})


@user_passes_test(lambda user: user.is_superuser,
                  login_url='user:page_not_found')
@login_required(login_url="login_system")
def update_active_collaborator(request, id):
    try:
        Collaborator.objects.filter(id=id).update(
            active=not Collaborator.objects.get(id=id).active)
    except Exception as e:
        print(f"Exceção ao atualizar a situação do colaborador{e}")
    return redirect('collaborator:update_collaborator')
