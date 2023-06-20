from django.shortcuts import render
from django.shortcuts import render,redirect
from .forms import *
from .models import Purchase
from .models import PurchaseItems
from Product.forms import searchProductForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import user_passes_test
from django.db.models import Q

@user_passes_test(lambda user: user.is_staff or user.is_superuser ,login_url='page_not_found')      
@login_required(login_url="login_system")
def main_menu_purchase(request):
     return render(request,'purchase/main_menu_purchase.html',{'purchases':Purchase.objects.all()})

def save_purchase(request):
    try:
        if request.method == "POST":
            form = PurchaseForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Salvo com sucesso")
        else:
         form = PurchaseForm()
    except Exception as e:
        print(f"Exceção ao salvar um colaborador {e}")
        messages.warning(request, "Ocorreu um erro ao registrar o Produto")
    return render(request, 'purchase/save_purchase.html', {'form': form})
#-------------------------------------------------------------------------------------------------------
@user_passes_test(lambda user: user.is_staff or user.is_superuser ,login_url='page_not_found')      
@login_required(login_url="login_system")
def erase_purchase(request, id):
    print(request.method)
    try:
        Purchase.objects.filter(id=id).update(is_deleted=True)
    except Exception as e:
        print(f"Exceção no deletar produto {e}")
    return redirect('purchase:main_menu_purchase')

@user_passes_test(lambda user: user.is_staff or user.is_superuser ,login_url='page_not_found')      
@login_required(login_url="login_system")
def update_purchase(request,id):
    purchase_selected = Purchase.objects.get(id=id)
    form = PurchaseForm(request.POST or None, instance=purchase_selected)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Atualizado com sucesso")
            return redirect('purchase:main_menu_purchase')
        else:
            messages.warning(request, "Dados Invalido")
        
    return render(request,'purchase/update_purchase.html',{'form':form})

 

 

     
     
     
