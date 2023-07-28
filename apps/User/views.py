import hashlib
from sqlite3 import IntegrityError

from Collaborator.models import Collaborator
from django.contrib import messages
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import redirect, render
from User.tasks import confirm_register
from validate_docbr import CPF

from .forms import (registerUserForm, updateUserPasswordForm,
                    updateWithoutPasswordForm)
from .models import User


@receiver(post_save, sender=Collaborator)
def alert_create_user(sender, instance, created, *args, **kwargs):
    if created:
        user = User.objects.get(id=instance.user.pk)
        confirm_register.delay(email=user.email, nameUser=instance.name,
                               username=user.username, password=user.password)


def generate_md5(text):
    md5_hash = hashlib.md5()
    md5_hash.update(text.encode('utf-8'))
    md5_hex = md5_hash.hexdigest()

    return md5_hex


@user_passes_test(lambda user: user.is_superuser,
                  login_url='user:page_not_found')
@login_required(login_url="login_system")
def save_user(request):

    try:
        form = None
        if request.method == "POST":
            form = registerUserForm(request.POST)
            if form.is_valid():

                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                password_check = form.cleaned_data['password_check']
                if password != password_check:
                    messages.warning(request, "A senhas devem ser iguais")
                else:
                    validation = CPF()
                    is_staff = form.cleaned_data['is_staff']
                    email = form.cleaned_data['email']
                    cpf_mask = form.cleaned_data['cpf']
                    cpf = cpf_mask.replace(
                        ".", "").replace(".", "").replace("-", "")
                    name = form.cleaned_data['name']
                    md5 = generate_md5(cpf_mask)
                    if validation.validate(cpf_mask):
                        if not Collaborator.objects.filter(cpf=cpf).exists():
                            user = User.objects.create(username=username,
                                                       password=password,
                                                       email=email,
                                                       is_staff=is_staff)
                            Collaborator.objects.create(name=name,
                                                        cpf=cpf,
                                                        user=user,
                                                        cod_auth=md5)
                            user.set_password(password)
                            user.save()
                            messages.success(request, "Salvo com sucesso")
                            return redirect('user:main_menu_user')
                        else:
                            raise IntegrityError('O CPF já está registrado')
                    else:
                        messages.warning(request, "O CPF Inválido")
            else:
                messages.warning(request, "Formulario Invalido")
        else:
            form = registerUserForm()
    except (Exception, IntegrityError) as e:
        if 'username' in str(e):
            messages.warning(request,
                             "O nome de usuário já existe")
        if 'email' in str(e):
            messages.warning(request,
                             "O email já está registrado")
        else:
            print(f"Exceção ao salvar um Usuario - {e}")
            messages.warning(request, "O CPF já está registrado")

    return render(request, 'user/save_user.html', {'form': form})


@user_passes_test(lambda user: user.is_superuser,
                  login_url='user:page_not_found')
@login_required(login_url="login_system")
def erase_user(request, id):
    try:
        User.objects.filter(id=id).update(
            is_deleted=not User.objects.get(id=id).is_deleted)

    except (Exception, User.DoesNotExist) as e:
        print(f"Exceção ao excluir Usuario - {e}")
        messages.warning(request, "Erro ao excluir o usuario")
        return redirect('user:main_menu_user')
    messages.success(request, "Deletado com sucesso")
    return redirect('user:main_menu_user')


@user_passes_test(lambda user: user.is_superuser,
                  login_url='user:page_not_found')
@login_required(login_url="login_system")
def update_user(request, id):
    try:
        obj_user = User.objects.get(id=id)
        form = updateWithoutPasswordForm(request.POST or None,
                                         instance=obj_user)
        if request.method == "POST":
            try:
                if form.is_valid():
                    obj_user.email = form.cleaned_data['email']
                    obj_user.username = form.cleaned_data['username']
                    obj_user.save()
                    messages.success(request, "Usuario Atualizado com sucesso")
                    return redirect('user:main_menu_user')
            except Exception as e:
                if 'username' in str(e):
                    print(f'O nome de usuário já existe {e}')
                    messages.warning(request, "O nome de usuário já existe")
                if 'email' in str(e):
                    print(f'O email já está registrado {e}')
                    messages.warning(request, "O email já está registrado")
    except User.DoesNotExist and Exception as e:
        print(f"Exceção no update de user  - {e}")
        messages.warning(request, "Erro ao atualizar o usuario")
    return render(request, 'user/update_user.html', {'form': form, 'id': id})


@user_passes_test(lambda user: user.is_superuser,
                  login_url='user:page_not_found')
@login_required(login_url="login_system")
def update_user_password(request, id):

    form = updateUserPasswordForm()
    if request.method == "POST":
        form = updateUserPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['password']
            new_password_check = form.cleaned_data['password_check']
            if new_password == new_password_check:
                user = User.objects.get(id=id)
                user.set_password(new_password)
                user.save()
                messages.success(request, "Atualizado com sucesso")
                return redirect('user:main_menu_user')
            else:
                messages.warning(request, "A senhas devem ser iguais")

    return render(request, 'user/update_user _password.html', {'form': form})


@user_passes_test(lambda user: user.is_superuser,
                  login_url='user:page_not_found')
@login_required(login_url="login_system")
def main_menu_user(request):
    if 'filter' in request.session:
        filter = request.session['filter']
    else:
        filter = None

    if filter:
        users = User.objects.filter(username__startswith=filter,
                                    is_deleted=True)
        request.session['filter'] = None
    else:
        users = User.objects.filter(is_deleted=True)

    return render(request, 'user/main_menu_users.html', {'users': users})


def page_not_found(request):
    return render(request, 'page_not_found.html')
