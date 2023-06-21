from django.shortcuts import render
from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from Product.forms import searchProductForm
from Product.models import Product
from .models import PurchaseItems

def save_purchase(request,product:Product = None):
    purchaseItems:PurchaseItems = []
    form_code_bar=None
    try:
        if request.method == "POST":
            form = PurchaseForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Salvo com sucesso")
        else:
          form_code_bar = searchProductForm()
          form = PurchaseRegisterForm()
          if product != None:
            purchaseItems.append(product) 
    except Exception as e:
        print(f"Exceção ao salvar um colaborador {e}")
        messages.warning(request, "Ocorreu um erro ao registrar o Produto")
        
    return render(request, 'purchase/save_purchase.html', {'form': form,'form_code_bar':form_code_bar,"purchaseItems":purchaseItems})


def find_product(request) -> Product:
    code_bar = None
    if request.method == "POST":
        form = searchProductForm()
        if form.is_valid():
               code_bar = form.cleaned_data['code_bar']
               if code_bar != None:
                   Product.objects.get(code_bar=code_bar)
    return save_purchase(request, code_bar)
  
            

     
     
     
