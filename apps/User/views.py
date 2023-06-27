from sqlite3 import IntegrityError
from django.shortcuts import render,redirect
from .forms import registerUserForm,authForm,updateWithoutPasswordForm,updateUserPasswordForm,findByUsernameForm
from django.contrib.admin.views.decorators import user_passes_test
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import logout,login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from Purchase.models import Purchase
from django.contrib import messages
from django.db.models import Q
from Collaborator.models import Collaborator
from Purchase.models import DeadLine
from datetime import datetime
from .models import User
from datetime import datetime
from datetime import date
from django.db.models import Sum
from fpdf import FPDF
import calendar

def generate_reports(request):
    deadLine = DeadLine.objects.get(id=1).DAY
    today = datetime.now().day
    
    if today > deadLine:
        start_date = date(datetime.now().year,datetime.now().month ,(deadLine+1))
        
        if datetime.now().month+1 == 13:
            end_date = date((datetime.now().year+1),1 ,today)
        else: 
            end_date = date(datetime.now().year,(datetime.now().month+1),today)
            
    else:
        start_date = date(datetime.now().year,(datetime.now().month-1) ,(deadLine+1))
        end_date = date(datetime.now().year,datetime.now().month,today)
        
    listPurchases = Purchase.objects.filter(date_purchase__range=(start_date, end_date))

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 10)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 10, 'Vendas Referência Atual', 1, 1, 'C', 1)
    for purchase in listPurchases:
        purchase_date = purchase.date_purchase.strftime('%d/%m/%Y')
        pdf.cell(0, 10, f"Colaborador: {purchase.collaborator},Data:{purchase_date},Preço: {purchase.product}", 1, 1, 'L', 1)

    pdf.cell(0, 10, f'Total: {current_billing()}', 1, 0, 'C', 1)

    pdf.output('test.pdf')

    return redirect('user:initial_page')

def current_month_range():
    """Obtém a quantidade de dias do mês atual.

    Retorna o número de dias do mês atual com base na data atual.

    Returns:
        int: Número de dias do mês atual.
    """
    current_month = datetime.now().month
    current_year = datetime.now().year
    number_of_days = calendar.monthrange(current_year, current_month)[1]
    
    return number_of_days


def next_month_range():
    """Obtém a quantidade de dias do próximo mês.

    Retorna o número de dias do próximo mês com base na data atual.

    Returns:
        int: Número de dias do próximo mês.
    """
    next_month = datetime.now().month
    next_year = datetime.now().year
    
    if next_month > 12:
        next_month = 1
        next_year += 1
        
    number_of_days = calendar.monthrange(next_year, (next_month+1))[1]
    return number_of_days


def current_billing():
    """Calcula o total gasto no período de faturamento atual.

    A função determina o período de faturamento com base na data atual e recupera as compras feitas nesse período.
    Em seguida, calcula o total gasto somando os preços dos itens comprados.

    Returns:
        Decimal: O total gasto no período de faturamento atual.
    """
    deadLine = DeadLine.objects.get(id=1).DAY
    today = datetime.now().day
    
    if today > deadLine:
        start_date = date(datetime.now().year,datetime.now().month ,(deadLine+1))
        
        if datetime.now().month+1 == 13:
            end_date = date((datetime.now().year+1),1 ,today)
        else: 
            end_date = date(datetime.now().year,(datetime.now().month+1),today)
            
    else:
        start_date = date(datetime.now().year,(datetime.now().month-1) ,(deadLine+1))
        end_date = date(datetime.now().year,datetime.now().month,today)
        
    listPurchases = Purchase.objects.filter(date_purchase__range=(start_date, end_date))
    total_spended = listPurchases.aggregate(total=Sum('purchaseitem__price'))['total']
    
    return total_spended


@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')   
def initial_page(request):
    """Exibe a página inicial e constrói os dados do dashboard.

    Args:
        request (HttpRequest): A requisição HTTP recebida.

    Returns:
        HttpResponse: A resposta HTTP renderizada como HTML.
    """
    deadLine = DeadLine.objects.get(id=1).DAY
    today = datetime.now().day
    if today > deadLine:
        days_left_next_month = (next_month_range()-(next_month_range()-deadLine))
        days_left_current_month = (current_month_range()-today)
        dias = days_left_next_month + days_left_current_month
    else:
        dias = current_month_range()-today
        
    return render(request,'dashboard.html',{'dias':dias,'current_billing':current_billing()})

def login_system(request):
    """Gerencia o sistema de login do usuário.

    Esta função lida com a lógica de autenticação do usuário. Se o usuário já estiver autenticado,
    redireciona para a página inicial. Caso contrário, trata a requisição de login, verifica as credenciais
    do usuário e realiza o login se as credenciais forem válidas.

    Args:
        request (HttpRequest): A requisição HTTP recebida.

    Returns:
        HttpResponse: A resposta HTTP renderizada como HTML.
    """
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
                    return redirect('user:initial_page')
                else:
                    messages.warning(request, "Usuario ou Senha Errados.")
            else:
                messages.warning(request, "Credenciais inválidas.")
    except Exception as e :
        print(f"Exceção ao tentar fazer o login - {e}")
        
    return render(request, 'login.html', {'form': form})


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


def logout_system(request):
    """_summary_

    Args:
        request (_type_): Requisição do Usuario
        para realizar o logout do user logado
    Returns:
        Redirect: Vai para a pagina inicial, login da aplicação
    """
    logout(request)
    return redirect('user:initial_page')

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
        print(f"Exceção ao deletar Usuario - {e}")
        messages.error(request,"Erro ao deletar o usuario, por favor contate o suporte")
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
                        else:
                            messages.warning(request, "Username ja existe")
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
    return redirect('page_not_found')
     
     
     