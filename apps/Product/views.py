from django.shortcuts import render
from django.shortcuts import render,redirect
from .forms import searchProductForm, registerProductForm
from .models import Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import user_passes_test
from django.db.models import Q

@user_passes_test(lambda user: user.is_superuser,login_url='user:page_not_found')     
@login_required(login_url="login_system")
def main_menu_product(request,name=None):
    form = searchProductForm()
    if not name:
        products = Product.objects.all()
    else:
        form = searchProductForm(request.POST)
        products = Product.objects.filter(name__startswith=name)
    
    return render(request,'product/main_menu_product.html',{'products':products,'form':form})

@user_passes_test(lambda user: user.is_superuser,login_url='user:page_not_found')    
@login_required(login_url="login_system")
def save_product(request):
    try:
        if request.method == "POST":
            form = registerProductForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Salvo com sucesso")
                return redirect ('product:main_menu_product')
        else:
         form = registerProductForm()
    except Exception as e:
        print(f"Exceção ao salvar um colaborador {e}")
        messages.warning(request, "Ocorreu um erro ao registrar o Produto")
    return render(request, 'product/save_product.html', {'form': form})

@user_passes_test(lambda user: user.is_superuser,login_url='user:page_not_found')        
@login_required(login_url="login_system")
def erase_product(request, id):
    print(request.method)
    try:
        Product.objects.filter(id=id).update(is_deleted=True)
    except Exception as e:
        print(f"Exceção no deletar produto {e}")
    return redirect('product:main_menu_product')

@user_passes_test(lambda user: user.is_superuser,login_url='user:page_not_found')      
@login_required(login_url="login_system")
def update_product(request,id):
    product_selected = Product.objects.get(id=id)
    form = registerProductForm(request.POST or None, instance=product_selected)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Atualizado com sucesso")
            return redirect('product:main_menu_product')
        else:
            messages.warning(request, "Dados Invalido")
        
    return render(request,'product/update_product.html',{'form':form})

@user_passes_test(lambda user: user.is_superuser,login_url='user:page_not_found')    
@login_required(login_url="login_system")
def main_menu_product_with_filter(request):
    try:
        if request.method == "POST":
            form = searchProductForm(request.POST)
            if form.is_valid():
                name = None
                name = form.cleaned_data['name']
                
    except Exception as e:
        print(f"Exceção no filtar produco por codigo de barras - {e}")
    return main_menu_product(request,name)
        

 

     
     
     
