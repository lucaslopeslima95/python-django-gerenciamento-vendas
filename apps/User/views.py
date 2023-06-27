from django.shortcuts import render
from django.shortcuts import render,redirect
from .forms import registerUserForm,authForm,updateWithoutPasswordForm,updateUserPasswordForm
from .models import User
from django.contrib.auth import logout,login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import user_passes_test
from django.db.models import Q
from django.dispatch import receiver
from Collaborator.models import Collaborator
from django.db.models.signals import post_save
from Purchase.models import DeadLine
from datetime import datetime
import calendar
from datetime import datetime
from datetime import date
from Purchase.models import Purchase,PurchaseItem
from django.db.models import Sum
from Product.models import Product
from fpdf import FPDF


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
    pdf.set_font('Arial', 'B',10)
    pdf.set_fill_color(240,240,240)
    pdf.cell(0,10,'Vendas Referência Atual',1,0,'C',1)
    for purchase in listPurchases:
        pdf.cell(0,10,f" Colaborador: {purchase.collaborator}, {purchase.date_purchase}, {purchase.product}",1,1,'L',1)
    
    pdf.cell(0,10,f'Total: { current_billing()}',1,0,'C',1)
   
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
    """_summary_

    Args:
        request (_request_): Essa def recebe apenas a requisição 
        como parametro e apresenta a pagina inicial com 
        retorno, aqui tambem é contruido os dados que constituem
        o dashboar
    Returns:
        _Render_: O retorno sempre será do tipo html render
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



@user_passes_test(lambda user: user.is_superuser,login_url='user:page_not_found')   
@login_required(login_url="login_system")
def save_user(request):
    try:
        form=None
        if request.method == "POST":
            form = registerUserForm(request.POST)
            if form.is_valid():
                    username = form.cleaned_data['username']
                    password = form.cleaned_data['password']
                    password_check = form.cleaned_data['password_check']
                    
                    if User.objects.filter(username=username).exists():
                        messages.warning(request, "Usuario já existe")
                    elif password != password_check:
                        messages.success(request, "As senha não coincidem")
                        
                    else:
                        is_staff = form.cleaned_data['is_staff']
                        email = form.cleaned_data['email']
                        cpf = form.cleaned_data['cpf']
                        name = form.cleaned_data['name']
                        user =  User.objects.create(username=username, password=password, email=email,is_staff=is_staff)
                        Collaborator.objects.create(name=name,cpf=cpf, user=user)
                        user.set_password(password)
                        user.save()
                        messages.success(request, "Salvo com sucesso")
                        
                        return redirect('user:main_menu_user')
        else:
         form = registerUserForm()
    except Exception as e:
        print(f"Exceção ao salvar um Usuario - {e}")
        messages.warning(request, "Ocorreu um erro ao registrar o usuário")
    return render(request, 'user/save_user.html', {'form': form})


def logout_system(request):
    logout(request)
    return redirect('user:initial_page')

@user_passes_test(lambda user: user.is_superuser,login_url='user:page_not_found')   
@login_required(login_url="login_system")
def erase_user(request, id):
    try:
        user = User.objects.get(id=id)
        user.delete()
    except Exception as e:
        print(e)
    return redirect('user:main_menu_user')

@user_passes_test(lambda user: user.is_superuser,login_url='user:page_not_found')     
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
       print(f"Exceção no update de user  - {e}")
       

    return render(request,'user/update_user.html',{'form':form})



@user_passes_test(lambda user: user.is_superuser,login_url='user:page_not_found')    
@login_required(login_url="login_system")
def update_user_password(request,id):
    form = updateUserPasswordForm()
    if request.method == "POST":
        form = updateUserPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['password']
            user = User.objects.get(id=id)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Atualizado com sucesso")
            return redirect('user:main_menu_user')
    return render(request,'user/update_user.html',{'form':form})

 
@user_passes_test(lambda user: user.is_superuser,login_url='user:page_not_found')    
@login_required(login_url="login_system")
def main_menu_user(request):
     return render(request,'user/main_menu_users.html',{'users':User.objects.all()})
 
 
def page_not_found(request):
   return render(request,'page_not_found.html')
     
     
     