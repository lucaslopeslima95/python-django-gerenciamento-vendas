from django.shortcuts import render
from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from Purchase.forms import searchProductToPurchaseForm
from Product.models import Product
from .models import PurchaseItem

listPurchaseItems = []

def save_purchase(request,listPurchaseItems = []):
    form_code_bar = searchProductToPurchaseForm()
    try:
        if request.method == "POST":
            form = PurchaseItemForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Salvo com sucesso")
    except Exception as e:
        print(f"Exceção ao salvar um colaborador {e}")
        messages.warning(request, "Ocorreu um erro ao registrar o Produto")
        
    return render(request, 'purchase/save_purchase.html', {'form_code_bar':form_code_bar,"purchaseItems":listPurchaseItems})

def find_product(request):
    try:
        form = searchProductToPurchaseForm(request.POST)
        if request.method == "POST":
            if form.is_valid():
                code_bar = form.cleaned_data['code_bar']
                quantity = form.cleaned_data['quantity']
                
                for item in listPurchaseItems:
                    if item.fk_product.code_bar == code_bar:
                        quantity_current = int(item.quantity)
                        quantity_current += int(quantity)
                        item.quantity = quantity_current
                        return save_purchase(request,listPurchaseItems)
                                 
                if code_bar != None:
                    product = Product.objects.get(code_bar=code_bar)
                    purchaseItem = PurchaseItem()  
                    purchaseItem.fk_product = product
                    purchaseItem.price = product.price
                    purchaseItem.quantity = quantity
                    listPurchaseItems.append(purchaseItem)
                    
    except Exception as e:
        print(f" Exceção no procurar produto {e}")
    request.method = "GET"   
    return save_purchase(request,listPurchaseItems)
  
            
def remove_product_purchase(request,id):
    for produto in listPurchaseItems:
        if id == produto.fk_product.id:
            listPurchaseItems.remove(produto)
    return save_purchase(request,listPurchaseItems)
     
def clean_all_products_purchase(request):
     listPurchaseItems = []
     return save_purchase(request,listPurchaseItems)
