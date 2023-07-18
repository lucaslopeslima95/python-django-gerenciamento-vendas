from Collaborator.models import Collaborator
from django.contrib import messages
from django.contrib.auth import authenticate
from django.db.models import Sum
from django.shortcuts import redirect, render
from Product.models import Product, StoreStock
from Purchase.models import Purchase, PurchaseItem
from Purchase.PurchaseService.calculateExpends import (
    calculates_and_returns_current_referral_spending,
    calculates_and_returns_last_reference_spend)
from Purchase.tasks import confirm_purchase
from User.forms import authForm

from .DTO.PurchaseItemDTO import PurchaseItemDTO
from .forms import searchProductToPurchaseForm


def initial_page_purchase(request):
    cart = PurchaseItemDTO()
    form_code_bar = searchProductToPurchaseForm()
    puchase_list_total_value = None
    
    if request.method == "GET":
        try:
            puchase_list_total_value = 0
            for i in cart.products:
                puchase_list_total_value += i.product.price
            
        except Exception as e:
            print(f"Exceção ao salvar um colaborador {e}")
            messages.warning(request, "Ocorreu um erro ao adicionar o Produto")
        
    return render(request, 'purchase/initial_purchase.html',
               {
                'form_code_bar':form_code_bar,
                'cart':cart,
                'total':puchase_list_total_value,
                'authForm':authForm
                })

def finish_purchase(request):
    cart = PurchaseItemDTO()
    try:
        if request.method == "POST":
                form = authForm(request.POST)
                if form.is_valid():
                    username = form.cleaned_data['username']
                    password = form.cleaned_data['password']
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        if len(cart.products)==0:
                            messages.warning(request,"Nenhum Produto Adicionado")
                            return redirect('purchase:initial_page_purchase')
                        collaborator = Collaborator.objects.get(user=user.id)
                        if collaborator.active and save_purchase(collaborator):
                            cart.products.clear()                                 
                            messages.success(request, "Salvo com Sucesso.")
                            
                            current_spends = calculates_and_returns_current_referral_spending(collaborator).aggregate(total=Sum('purchaseitem__price'))['total']
                            last_spends = calculates_and_returns_last_reference_spend(collaborator).aggregate(total=Sum('purchaseitem__price'))['total']
                            
                            if current_spends and last_spends:
                                request.session['total_spends_current'] = float(current_spends)
                                request.session['total_spends_last_referred'] = float(last_spends)
                                request.session['show_expends'] = True
                            else:
                                 request.session['total_spends_current'] = 0.0
                                 request.session['total_spends_last_referred'] = 0.0
                                 request.session['show_expends'] = True
                        else:
                            cart.products.clear()
                            messages.warning(request, "Colaborador Inativo, por favor entre em contato com o RH")
                            return redirect('purchase:initial_purchase')
                            
                    else:
                        messages.warning(request, "Usuario ou Senha Errados.")
                        return redirect('purchase:initial_page_purchase')
                else:
                    messages.warning(request, "Credenciais inválidas.")
    except (Exception,Product.DoesNotExist) as e:
        print(f" Exceção ao finalizar a compra - {e}")
        
    return redirect('purchase:initial_page_purchase')

    
def find_product(request):
    in_cart = PurchaseItemDTO()
    if request.method == "POST":
        product = None
        try:
            form = searchProductToPurchaseForm(request.POST)
            if form.is_valid():
                code_bar = form.cleaned_data['code_bar']
                if code_bar != None:
                    code_bar_cleaned = code_bar.replace("-","").replace("-","").replace("-","")
                    product = Product.objects.get(code_bar=code_bar_cleaned)
                    stock = StoreStock.objects.get(product__id=product.id)
                    if stock.stock_quantity < 1:
                         messages.warning(request, f"O {product.name} não possui unidades disponiveis no momento")
                    else:    
                        purchaseItem = PurchaseItem()  
                        purchaseItem.product = product
                        purchaseItem.price = product.price
                        in_cart.products.append(purchaseItem)
        except (Product.DoesNotExist,Exception) as e:
            print(f"Exceção ao procurar produto {e}")
            messages.warning(request, "Produto não encontrado")
        

    return redirect('purchase:initial_page_purchase')
     
     
def remove_product_purchase(request,id):
    in_cart = PurchaseItemDTO()
    in_cart.products.pop((id-1))
    return redirect('purchase:initial_page_purchase')
    
    
def clean_all_products_purchase(request):
    in_cart = PurchaseItemDTO()
    in_cart.products.clear()
    request.session['total_spends_current'] = 0.0
    request.session['total_spends_last_referred'] = 0.0
    request.session['show_expends'] = False
    return redirect('purchase:initial_page_purchase')


def save_purchase(collaborator:Collaborator) -> bool:
    try:
        purchase_itens = {}
        cart = PurchaseItemDTO()
        purchase = Purchase()
        
        purchase.collaborator = collaborator
    
        purchase.save()
      
        for item in cart.products:
         
           if not item.product.name in purchase_itens:
                
                purchase_itens[item.product.name] = {
                    'id':int(item.product.pk),
                    'price':float(item.product.price),
                    'category':str(item.product.category),
                    'quantity':1
                }
            
           else:
                  
               purchase_itens[item.product.name]['quantity'] += 1 
        
        for product in purchase_itens.items():  
           
           
            if not product[1]['category'] == 'Ingressos'\
                or product[1]['category'] == 'Camisetas':
                     update_quantity(product[1]) 
                
            purchaseItem = PurchaseItem.objects.create(
                product=Product.objects.get(id=product[1]['id']),  
                price=product[1]['price'],
                purchase=purchase,
                quantity=product[1]['quantity']
            )
            purchaseItem.save()
       
        confirm_purchase.delay(email=collaborator.user.email, nameUser=collaborator.name,purchase_itens=purchase_itens)
        
    except Exception as e:
        print(f" Exceção ao salvar a compra - {e}")
    return True  
   
    
def update_quantity(product: dict) -> None:
    try:
        stock = StoreStock.objects.get(product__id=product['id'])
        
        new_quantity = stock.stock_quantity - product['quantity']
        
        stock.stock_quantity = new_quantity
        
        stock.save()
    except StoreStock.DoesNotExist:
        print(f"StoreStock não encontrado para o produto com ID {product}")
    except Exception as e:
        print(f"Exceção ao atualizar a quantidade do produto - {e}")
        
        
def check_balance(request):
    if request.method == "POST":
        form = authForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                collaborator = Collaborator.objects.get(user=user.id)
                if collaborator.active:          
                    request.session['total_spends_current'] = float(calculates_and_returns_current_referral_spending(collaborator).aggregate(total=Sum('purchaseitem__price'))['total'])
                    request.session['total_spends_last_referred'] = float(calculates_and_returns_last_reference_spend(collaborator).aggregate(total=Sum('purchaseitem__price'))['total'])
                    request.session['only_consult'] = True
                else:
                    messages.warning(request,"Perfil de Colaborador Inativo, entre em contato com o RH")
            else:
                messages.warning(request,"Credenciais Inválidas")
    return redirect('purchase:initial_page_purchase')


def clean_consult(request):
    request.session['total_spends_current'] = 0.0
    request.session['total_spends_last_referred'] = 0.0
    request.session['only_consult'] = False
    return redirect('purchase:initial_page_purchase')
