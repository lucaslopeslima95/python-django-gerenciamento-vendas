from django.shortcuts import render
from django.shortcuts import render
from .forms import searchProductToPurchaseForm
from django.contrib import messages
from Product.models import Product
from User.forms import authForm
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from .DTO.PurchaseItemDTO import PurchaseItemDTO
from Collaborator.models import Collaborator
from Purchase.models import Purchase,PurchaseItem
listPurchaseItems = []
    
def initial_page_purchase(request,listPurchaseItems = []):
    try:
        form_code_bar = searchProductToPurchaseForm()
        puchase_list_total_value = 0
        for i in listPurchaseItems:
            puchase_list_total_value += i.total_cost
    except Exception as e:
        print(f"Exceção ao salvar um colaborador {e}")
        messages.warning(request, "Ocorreu um erro ao registrar o Produto")
    return render(request, 'purchase/initial_purchase.html', {'form_code_bar':form_code_bar,"purchaseItems":listPurchaseItems,"total":puchase_list_total_value,"authForm":authForm })


def finish_purchase(request):
    
    if len(listPurchaseItems) == 0:
        messages.warning(request, "Não é possivel Finalizar Sem Adicionar Produtos")
        return initial_page_purchase(request)
    
    if request.method == "POST":
            form = authForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return initial_page_purchase(request)
                else:
                    messages.warning(request, "Usuario ou Senha Errados.")
            else:
                messages.warning(request, "Credenciais inválidas.")
    return initial_page_purchase(request)
    

def find_product(request):
    try:
        form = searchProductToPurchaseForm(request.POST)
        if request.method == "POST":
            if form.is_valid():
                code_bar = form.cleaned_data['code_bar']
                quantity = form.cleaned_data['quantity']
                for item in listPurchaseItems:
                    if item.product.code_bar == code_bar:
                        quantity_current = int(item.quantity)
                        quantity_current += int(quantity)
                        item.quantity = quantity_current
                        item.total_cost = (quantity_current*item.price)
                        return initial_page_purchase(request,listPurchaseItems)
                                
                if code_bar != None:
                    try:
                        product = Product.objects.get(code_bar=code_bar)
                    except Exception as e:
                        print(f"Produto Nao Existe - {e}")
                        messages.warning(request, "Produto não encontrado")
                        
                    purchaseItem = PurchaseItemDTO()  
                    purchaseItem.product = product
                    purchaseItem.price = product.price
                    purchaseItem.quantity = quantity
                    purchaseItem.total_cost = (quantity*product.price)
                    listPurchaseItems.append(purchaseItem)
    except Exception as e:
        print(f" Exceção no procurar produto - {e}")
    request.method = "GET"   
    return initial_page_purchase(request,listPurchaseItems)

     
def remove_product_purchase(request,id):
    for produto in listPurchaseItems:
        if id == produto.product.id:
            listPurchaseItems.remove(produto)
    return initial_page_purchase(request,listPurchaseItems)
    
    
def clean_all_products_purchase(request):
    listPurchaseItems = []
    return initial_page_purchase(request,listPurchaseItems)
