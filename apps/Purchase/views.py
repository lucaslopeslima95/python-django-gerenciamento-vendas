from django.shortcuts import render,redirect
from Purchase.PurchaseService.calculateExpends import calculates_and_returns_current_referral_spending, calculates_and_returns_last_reference_spend
from .forms import searchProductToPurchaseForm
from django.contrib import messages
from Product.models import Product
from User.forms import authForm
from django.contrib.auth import authenticate
from .DTO.PurchaseItemDTO import PurchaseItemDTO
from Collaborator.models import Collaborator
from Purchase.models import Purchase,PurchaseItem


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
                        employee_who_made_the_purchase = Collaborator.objects.get(user=user.id)
                        if employee_who_made_the_purchase.active:
                            if save_purchase(employee_who_made_the_purchase):
                                cart.total_spends_current = calculates_and_returns_current_referral_spending(employee_who_made_the_purchase)
                                cart.total_spends_last_referred = calculates_and_returns_last_reference_spend(employee_who_made_the_purchase)
                                cart.products.clear()
                                messages.success(request, "Salvo com Sucesso.")
                                cart.show_spends = True
                                return redirect('purchase:initial_page_purchase')
                        else:
                            cart.products.clear()
                            messages.warning(request, "Colaborador Inativo, por favor entre em contato com o RH")
                            return redirect('purchase:initial_purchase')
                            
                    else:
                        cart.login_failed = True
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
                    product = Product.objects.get(code_bar=code_bar)    
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
    return redirect('purchase:initial_page_purchase')


def save_purchase(collaborator) -> bool:
    try:   
        set_products = {}
        purchase = Purchase()
        purchase.collaborator = collaborator
        purchase.save()
        cart = PurchaseItemDTO()
        set_products = cart.products
        for item in set_products:
            count =  0
         
            for product in cart.products:
                if item.id == product.id:
                    count += 1
         
            purchaseItem = PurchaseItem.objects.create(product=item.product,
                                        price=item.product.price,
                                        purchase=purchase,
                                        quantity=count)
            
            purchaseItem.save()
           
            
            
    except Exception as e:
        print(f" Exceção ao salvar a compra {e}")
    return True  
    
   