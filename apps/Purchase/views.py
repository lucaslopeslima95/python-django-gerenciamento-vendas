from django.shortcuts import render
from django.shortcuts import render
from .forms import searchProductToPurchaseForm
from django.contrib import messages
from Product.models import Product
from User.forms import authForm
from django.contrib.auth import authenticate
from .DTO.PurchaseItemDTO import PurchaseItemDTO
from Collaborator.models import Collaborator
from Purchase.models import Purchase,PurchaseItem
from User.models import User

listPurchaseItemsDTO = []

def initial_page_purchase(request,listPurchaseItemsDTO = [],login_failed=False):
    try:
        form_code_bar = searchProductToPurchaseForm()
        puchase_list_total_value = 0
        for i in listPurchaseItemsDTO:
            puchase_list_total_value += i.total_cost
    except Exception as e:
        print(f"Exceção ao salvar um colaborador {e}")
        messages.warning(request, "Ocorreu um erro ao registrar o Produto")
    return render(request, 'purchase/initial_purchase.html',
                  {'form_code_bar':form_code_bar,"purchaseItems":listPurchaseItemsDTO,"total":puchase_list_total_value,"authForm":authForm,"login_failed":login_failed })

def finish_purchase(request):
    if len(listPurchaseItemsDTO) == 0:
        messages.warning(request, "Não é possivel Finalizar Sem Adicionar Produtos")
        return initial_page_purchase(request)
    else:
        if request.method == "POST":
                form = authForm(request.POST)
                if form.is_valid():
                    username = form.cleaned_data['username']
                    password = form.cleaned_data['password']
                    print('--------------------------------------------------')
                    print(username)
                    print(password)
                    collaborator = authenticate(request, username=username, password=password)
                    print(collaborator)
                    
                    if collaborator is not None:
                        if save_purchase(username):
                            messages.success(request, "Salvo com Sucesso.")
                            return initial_page_purchase(request)
                            
                            #implementar Logica para mostrar o consumo da referencia atual
                    else:
                        login_failed = True
                        messages.warning(request, "Usuario ou Senha Errados.")
                        return initial_page_purchase(request,login_failed=login_failed,listPurchaseItemsDTO=listPurchaseItemsDTO)
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
                for item in listPurchaseItemsDTO:
                    if item.product.code_bar == code_bar:
                        quantity_current = int(item.quantity)
                        quantity_current += int(quantity)
                        item.quantity = quantity_current
                        item.total_cost = (quantity_current*item.price)
                        return initial_page_purchase(request,listPurchaseItemsDTO)
                                
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
                    listPurchaseItemsDTO.append(purchaseItem)
    except Exception as e:
        print(f" Exceção no procurar produto - {e}")
    request.method = "GET"   
    return initial_page_purchase(request,listPurchaseItemsDTO)

     
def remove_product_purchase(request,id):
    for produto in listPurchaseItemsDTO:
        if id == produto.product.id:
            listPurchaseItemsDTO.remove(produto)
    return initial_page_purchase(request,listPurchaseItemsDTO)
    
    
def clean_all_products_purchase(request):
    listPurchaseItemsDTO.clear()
    return initial_page_purchase(request,listPurchaseItemsDTO)


def save_purchase(username):
    try:
        print(User.objects.filter(username=username))
        collaborator = User.objects.filter(username=username)
        purchase_obj = Purchase()
        purchase_obj.save()
        purchase_obj.fk_colaborattor.add(collaborator)
        
        for itemPurchaseDTO in listPurchaseItemsDTO:
            purchaseItem = PurchaseItem()
            purchaseItem.fk_product = itemPurchaseDTO.product
            purchaseItem.price = itemPurchaseDTO.price
            purchaseItem.quantity =  itemPurchaseDTO.quantitty
            purchaseItem.fk_purchase = purchase_obj
            purchaseItem.fk_collaborator = collaborator
            purchaseItem.save()
    except Exception as e:
        print(f" Exceção ao salva os itens da compra - {e}")
    return True  

    