from django.shortcuts import render,redirect
from .forms import searchProductToPurchaseForm
from django.contrib import messages
from Product.models import Product
from User.forms import authForm
from django.contrib.auth import authenticate
from .DTO.PurchaseItemDTO import PurchaseItemDTO
from Collaborator.models import Collaborator
from Purchase.models import Purchase,PurchaseItem
from Purchase.models import DeadLine
from datetime import datetime
from datetime import date
from django.db.models import Sum


listPurchaseItemsDTO = []

def calculates_and_returns_current_referral_spending(employee_who_made_the_purchase:Collaborator):
    """Calcula e retorna o gasto atual com referências de um determinado colaborador.

    Args:
        employee_who_made_the_purchase (Collaborator): O colaborador que fez a compra.

    Returns:
        Decimal: O valor total gasto pelo colaborador em referências durante o período.
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
        
    listPurchases = Purchase.objects.filter(date_purchase__range=(
        start_date, end_date),
        collaborator__name=employee_who_made_the_purchase,
        )
    total_spended = listPurchases.aggregate(total=Sum('purchaseitem__price'))['total']
    return total_spended
    
    
def calculates_and_returns_past_reference_spend(employee_who_made_the_purchase:Collaborator):
    """Calcula o preço total das compras de um determinado colaborador em um período específico.

    Args:
        employee_who_made_the_purchase (str): Nome do colaborador que fez a compra.

    Returns:
        Decimal: O valor total gasto pelo colaborador em referências durante o período.
    """
    deadLine = DeadLine.objects.get(id=1).DAY
    today = datetime.now().day
    
    if today > deadLine:
        start_date = date(datetime.now().year, (datetime.now().month-2) ,(deadLine+1))
        end_date = date(datetime.now().year,(datetime.now().month-1) ,deadLine)
    else:
        start_date = date(datetime.now().year, (datetime.now().month-1) ,(deadLine+1))
        end_date = date(datetime.now().year,datetime.now().month,deadLine)
        
   
    try:
        listPurchases = Purchase.objects.filter(date_purchase__range=(
            start_date, end_date),
            collaborator__name=employee_who_made_the_purchase,
            )
    except Exception as e:
        print(f"Exceção ao buscar valores na referencia passada - {e}")
    if not listPurchases:
        return 0.0
    
    try:
        total_spended = listPurchases.aggregate(total=Sum('purchaseitem__price'))['total']
        if total_spended == None:
            total_spended = 0.0
            
    except Exception as e:
        print(f"Exceção ao somar os valores da referencia passada {e}")
    
    
    return total_spended
    
                        

def initial_page_purchase(request,listPurchaseItemsDTO = [],login_failed=False,total_spends_current=0.0,total_spends_last_referred=0.0,show_spends = False):
    
    """Página inicial de compra.

    Renderiza a página inicial de compra, exibindo o formulário para adicionar
    produtos pelo código de barras, a lista de itens de compra, o valor total da compra
    e o formulário de autenticação. Também recebe a lista de itens de compra, caso
    já exista algum item adicionado, e a flag `login_failed`, que indica se houve
    falha na autenticação do usuário.

    Args:
        request (HttpRequest): Objeto HttpRequest que contém os dados da requisição.
        listPurchaseItemsDTO (list, optional): Lista de itens de compra. Defaults to [].
        login_failed (bool, optional): Indica se houve falha na autenticação do usuário.
            Defaults to False.

    Returns:
        HttpResponse: Objeto HttpResponse que representa a resposta HTTP renderizada
        com a página inicial de compra.
    """
   
    form_code_bar = None
    puchase_list_total_value = None
    if request.method == "POST":
        form_code_bar = searchProductToPurchaseForm()
        try:
            puchase_list_total_value = 0
            for i in listPurchaseItemsDTO:
                puchase_list_total_value += i.total_cost
            
        except Exception as e:
            print(f"Exceção ao salvar um colaborador {e}")
            messages.warning(request, "Ocorreu um erro ao adicionar o Produto")
        
    return render(request, 'purchase/initial_purchase.html',
               {'form_code_bar':form_code_bar,
                'purchaseItems':listPurchaseItemsDTO,
                'total':puchase_list_total_value,
                'authForm':authForm,"login_failed":login_failed,
                'total_spends_current':total_spends_current,
                'total_spends_last_referred':total_spends_last_referred,
                'show_spends':show_spends})

def finish_purchase(request):
    """
    Finaliza a compra, salvando os itens no banco de dados e exibindo mensagens de sucesso ou erro.

    Args:
        request (HttpRequest): Objeto HttpRequest contendo os dados da requisição.

    Returns:
        HttpResponse: HttpResponse contendo a resposta da requisição.

    """
    try:
        if request.method == "POST":
                form = authForm(request.POST)
                if form.is_valid():
                    username = form.cleaned_data['username']
                    password = form.cleaned_data['password']
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        employee_who_made_the_purchase = Collaborator.objects.get(user=user.id)
                        if employee_who_made_the_purchase.active:
                            if save_purchase(employee_who_made_the_purchase,listPurchaseItemsDTO):
                                current = calculates_and_returns_current_referral_spending(employee_who_made_the_purchase)
                                last = calculates_and_returns_past_reference_spend(employee_who_made_the_purchase)
                                listPurchaseItemsDTO.clear()
                                messages.success(request, "Salvo com Sucesso.")
                                show_spends = True
                                return initial_page_purchase(request,total_spends_current=current,total_spends_last_referred=last,show_spends=show_spends)
                        else:
                            listPurchaseItemsDTO.clear()
                            messages.warning(request, "Colaborador Inativo, por favor entre em contato com o RH")
                            return redirect('purchase:initial_purchase')
                            
                    else:
                        login_failed = True
                        messages.warning(request, "Usuario ou Senha Errados.")
                        return initial_page_purchase(request,login_failed=login_failed,listPurchaseItemsDTO=listPurchaseItemsDTO)
                else:
                    messages.warning(request, "Credenciais inválidas.")
    except (Exception,Product.DoesNotExist) as e:
        print(f" Exceção ao finalizar a compra - {e}")
        
    return initial_page_purchase(request)
    

def find_product(request):
    """
    Busca um produto com base no código de barras informado.

    Args:
        request (HttpRequest): Objeto HttpRequest contendo os dados da requisição.

    Returns:
        HttpResponse: HttpResponse contendo a resposta da requisição.

    Raises:
        Product.DoesNotExist: Caso o produto não seja encontrado.
        Exception: Caso ocorra uma exceção durante a busca do produto.

    """
    if request.method == "POST":
        product = None
        try:
            form = searchProductToPurchaseForm(request.POST)
            if form.is_valid():
                code_bar = form.cleaned_data['code_bar']
                if code_bar != None:
                    product = Product.objects.get(code_bar=code_bar)    
                    purchaseItem = PurchaseItemDTO()  
                    purchaseItem.product = product
                    purchaseItem.price = product.price
                    purchaseItem.total_cost = product.price
                    listPurchaseItemsDTO.append(purchaseItem)
                        
        except (Product.DoesNotExist,Exception) as e:
            print(f"Exceção ao procurar produto {e}")
            messages.warning(request, "Produto não encontrado")
        

    return initial_page_purchase(request, listPurchaseItemsDTO)
     
def remove_product_purchase(request,id):
    """_summary_

    Args:
        request (_request_): Remove da list pelo id do produto
        obs: O comportamento do remove é remover apenas o primeiro
        produto que ele encontra, por isso ele não remover
        todos os produtos que existem iguais na list de 
        itens de compra
    Returns:
        _request_: Retorna a pagina inicial de compras com a list
        de inss de compra atualizada
    """
    for produto in listPurchaseItemsDTO:
        if id == produto.product.id:
            listPurchaseItemsDTO.remove(produto)
    return redirect('purchase:initial_page_purchase')
    
    
def clean_all_products_purchase(request):
    """_summary_

    Args:
        request (_request_): Limpar a list de itens adicionados a compra

    Returns:
        _request_: Retorna a pagina inicial de compras
    """
    listPurchaseItemsDTO.clear()
    return redirect('purchase:initial_page_purchase')


def save_purchase(collaborator,listPurchaseItemsDTO):
    """
    Salva a compra no banco de dados.

    Args:
        user (obj): Objeto do usuário que confirmou a compra com login e senha.
        listPurchaseItemsDTO (list): Lista de compras que foram adicionadas na lista de compras
            na tela de registro de compras.

    Returns:
        bool: True se a operação de salvar no banco de dados for bem-sucedida. Em caso de exceção,
            imprime a mensagem "Exceção ao salvar os itens da compra" seguida da exceção gerada.
    """
    try:
        purchase_obj = Purchase()
        purchase_obj.collaborator = collaborator
        purchase_obj.save()
        for itemPurchaseDTO in listPurchaseItemsDTO:
            purchaseItem = PurchaseItem()
            Product.objects.filter(id = itemPurchaseDTO.product.id ).update(\
            stock_quantity=(Product.objects.get(id = itemPurchaseDTO.product.id)\
                                                .stock_quantity-1))
            purchaseItem.product = itemPurchaseDTO.product
            purchaseItem.price = itemPurchaseDTO.price
            purchaseItem.purchase = purchase_obj
            purchaseItem.save()

            listPurchaseItemsDTO.clear()
    except Exception as e:
        print(f"Exceção ao salva os itens da compra - {e}")
    return True  

