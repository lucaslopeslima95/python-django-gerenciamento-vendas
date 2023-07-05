from sqlite3 import IntegrityError
from django.shortcuts import (render,
                              redirect)
from Purchase.PurchaseService.calculateExpends import get_data_to_generate_reports
from Purchase.PurchaseService.current_billing import current_billing
from Purchase.PurchaseService.months_range import current_month_range, next_month_range
from Purchase.PurchaseService.products_low_stock import products_low_stock
from User.emails.emails import confirm_register
from .forms import (registerUserForm,
                    updateWithoutPasswordForm,
                    updateUserPasswordForm,
                    findByUsernameForm,
                    reportsForm
                    )
from django.contrib.admin.views.decorators import user_passes_test
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from Collaborator.models import Collaborator
from Purchase.models import DeadLine
from datetime import datetime
from .models import User
from django.db.models.signals import post_save
from django.dispatch import receiver 

@csrf_protect
@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')   
def initial_page(request):
    """Exibe a página inicial e constrói os dados do dashboard.

    Args:
        request (HttpRequest): A requisição HTTP recebida.

    Returns:
        HttpResponse: A resposta HTTP renderizada como HTML.
    """
    if request.method == "GET":
        deadLine = DeadLine.objects.get(id=1).DAY
        today = datetime.now().day
        if today > deadLine:
            days_left_next_month = (next_month_range()-(next_month_range()-deadLine))
            days_left_current_month = (current_month_range()-today)
            dias = days_left_next_month + days_left_current_month
        else:
            dias = current_month_range()-today
            
    return render(request,'dashboard.html',{'dias':dias,'current_billing':current_billing(),'products_low_stock':products_low_stock()})


@receiver(post_save,sender=Collaborator)
def alert_create_user(sender,instance:Collaborator,created,*args,**kwargs):
    if created: 
        user = User.objects.get(id=instance.user.pk)
        confirm_register(email=user.email,nameUser=instance.name)
    
@csrf_protect
@user_passes_test(lambda user: user.is_superuser,login_url='user:page_not_found')   
@login_required(login_url="login_system")
def save_user(request):
    """Salva um novo usuário no sistema.

    Esta função trata o processo de registro de um novo usuário. Recebe os dados do formulário de registro,
    valida os campos, cria o usuário e o colaborador correspondente, define a senha e salva no banco de dados.

    Args:
        request (HttpRequest): A requisição HTTP recebida.

    Returns:
        HttpResponse: A resposta HTTP renderizada como HTML.
    """
    try:
        form=None
        if request.method == "POST":
            form = registerUserForm(request.POST)
            if form.is_valid():
                    username = form.cleaned_data['username']
                    password = form.cleaned_data['password']
                    password_check = form.cleaned_data['password_check']
                    if password != password_check:
                        messages.error(request,"A senhas devem ser iguais")
                    else:
                        is_staff = form.cleaned_data['is_staff']
                        email = form.cleaned_data['email']
                        cpf_with_mask = form.cleaned_data['cpf']
                        cpf = cpf_with_mask.replace(".", "").replace(".", "").replace("-", "")
                        name = form.cleaned_data['name']
                        user =  User.objects.create(username=username, password=password, email=email,is_staff=is_staff)
                        Collaborator.objects.create(name=name,cpf=cpf, user=user)
                        user.set_password(password)
                        user.save()
                        messages.success(request, "Salvo com sucesso")
                        
                        return redirect('user:main_menu_user')
        else:
         form = registerUserForm()
    except (Exception,IntegrityError) as e:
        print(f"Exceção ao salvar um Usuario - {e}")
        messages.warning(request, "Ocorreu um erro ao registrar o usuário, contate o suporte")
    return render(request, 'user/save_user.html', {'form': form})



@user_passes_test(lambda user: user.is_superuser,login_url='user:page_not_found')   
@login_required(login_url="login_system")
def erase_user(request, id):
    """
    Remove um usuário do sistema.

    Args:
        request (HttpRequest): O objeto de requisição HTTP recebido.
        id (int): O ID do usuário a ser removido.

    Returns:
        HttpResponseRedirect: Redireciona para a página principal de usuários.

    Raises:
        User.DoesNotExist: Se o usuário com o ID especificado não existe.
        Exception: Se ocorrer um erro não tratado durante o processo de remoção.

    """
    try:
        user = User.objects.get(id=id)
        user.delete()
    except (Exception,User.DoesNotExist) as e:
        print(f"Exceção ao excluir Usuario - {e}")
        messages.error(request,"Erro ao excluir o usuario, por favor contate o suporte")
    messages.success(request, "Deletado com sucesso")
    return redirect('user:main_menu_user')

@user_passes_test(lambda user: user.is_superuser,login_url='user:page_not_found')     
@login_required(login_url="login_system")
def update_user(request,id):
    """
    Atualiza as informações de um usuário existente.

    Args:
        request (HttpRequest): O objeto de requisição HTTP recebido.
        id (int): O ID do usuário a ser atualizado.

    Returns:
        HttpResponseRedirect: Redireciona para a página principal de usuários após a atualização.

    Raises:
        User.DoesNotExist: Se o usuário com o ID especificado não existe.
        Exception: Se ocorrer um erro não tratado durante o processo de atualização.

    """
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
                                return redirect('user:main_menu_user')    
                        else:
                            messages.warning(request, "Username ja existe")
                            return redirect('user:main_menu_user')
    except User.DoesNotExist and Exception as e:
       print(f"Exceção no update de user  - {e}")
       messages.error(request,"Erro ao atualizar o usuario, por favor contate o suporte")
    
       return redirect('user:main_menu_user')

    return render(request,'user/update_user.html',{'form':form})



@user_passes_test(lambda user: user.is_superuser,login_url='user:page_not_found')    
@login_required(login_url="login_system")
def update_user_password(request,id):
    """
    Atualiza a senha de um usuário.

    Args:
        request (HttpRequest): O objeto de requisição HTTP recebido.
        id (int): O ID do usuário cuja senha será atualizada.

    Returns:
        HttpResponseRedirect: Redireciona para a página principal de usuários após a atualização.

    """
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
                messages.error(request,"A senhas devem ser iguais")
                redirect('update_user_password')
                
    return render(request,'user/update_user.html',{'form':form})

@user_passes_test(lambda user: user.is_superuser,login_url='user:page_not_found')    
@login_required(login_url="login_system")
def main_menu_user_with_filter(request):
    try:
        username = None
        if request.method == "POST":
            form = findByUsernameForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
    except Exception as e:
        print(f"Exceção ao pegar o valor para filtrar o usuario pelo username")
    return main_menu_user(request,username)
    
    
 
@user_passes_test(lambda user: user.is_superuser,login_url='user:page_not_found')    
@login_required(login_url="login_system")
def main_menu_user(request,username_to_filter = None):
    """_summary_

    Args:
        request (HttpRequest): O objeto de requisição HTTP recebido.

    Returns:
        HttpResponseRedirect: Redireciona para a página principal de usuários após a atualização.
    """
    users = None
    if not username_to_filter:
        users = User.objects.all()
    else:
       users =  User.objects.filter(username__startswith=username_to_filter)
    return render(request,'user/main_menu_users.html',{'users':users,'findByUsernameForm':findByUsernameForm})
 
 
def page_not_found(request):
    """_summary_

    Args:
         request (HttpRequest): O objeto de requisição HTTP recebido.

    Returns:
       HttpResponseRedirect: Em caso de violação de permissão ou url errada é 
       redirecionado para a paginad e não encontrado que possui um botão 
       para o voltar a pagina de login
    """
    return render(request,'page_not_found.html')
     
def page_initial_reports(request):
    return render(request,'reports/individual_report.html',{'form':reportsForm()})

@user_passes_test(lambda user: user.is_superuser,login_url='user:page_not_found')    
@login_required(login_url="login_system")
def make_reports(request):
    try:
        form = reportsForm()
        if request.method == "POST":
            form = reportsForm(request.POST)
            if form.is_valid():
                start_date = form.cleaned_data["start_date"]
                end_date = form.cleaned_data["end_date"]
                if start_date > end_date:
                    messages.error(request,"A data de inicio deve ser maior que a data de fim")
                    return redirect('user:page_initial_reports')
                collaborator = form.cleaned_data["collaborator"]
                
            else:
                 messages.error(request,"Formulario Inválido")
                 return redirect('user:page_initial_reports')
             
    except Exception as e:
        if e is not None:
            print(f"Exceção ao gerar relatório no make reports - {e}")
    return get_data_to_generate_reports(collaborator=collaborator,start_date=start_date,end_date=end_date)
        
