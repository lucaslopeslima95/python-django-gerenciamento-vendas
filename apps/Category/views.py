from django.contrib import messages
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import registerCategoryForm,findByNameForm
from .models import Category


@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')     
@login_required(login_url="login_system")
def main_menu_category(request,name=None):
    form = findByNameForm()
    if not name:
        categorys = Category.objects.all().order_by('name')
    else:
        form = findByNameForm(request.POST)
        categorys = Category.objects.filter(name__startswith=name).order_by('name')
    
    return render(request,'category/main_menu_category.html',{'categorys':categorys,'form':form})

@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')    
@login_required(login_url="login_system")
def save_category(request):
    try:
        if request.method == "POST":
            form = registerCategoryForm(request.POST)
            if form.is_valid():
                code_bar_with_mask = form.cleaned_data['code_bar']
                code_bar = code_bar_with_mask.replace("-","").replace("-","").replace("-","")
                form.initial['code_bar'] = code_bar
                form.save()
                messages.success(request, "Salvo com sucesso")
                return redirect ('product:main_menu_product')
        else:
         form = registerCategoryForm()
    except Exception as e:
        print(f"Codigo de Barras ja existe {e}")
        messages.warning(request, "Codigo de Barras ja existe")
    return render(request, 'product/save_product.html', {'form': form})

@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')        
@login_required(login_url="login_system")
def erase_product(request, id):
    try:
        Product.objects.filter(id=id).update(is_deleted= not Product.objects.get(id=id).is_deleted)
    except Exception as e:
        print(f"Exceção no excluir produto {e}")
    return redirect('product:main_menu_product')

@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')      
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

@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')    
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
        

@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')    
@login_required(login_url="login_system")
def update_status_product(request,id):
    try:
        Product.objects.filter(id=id).update(active = not Product.objects.get(id=id).is_deleted)
    except Exception as e:
        print(f"Exceção ao atualizar a situação do produto - {e}")
    return redirect('product:main_menu_product')

     
     
     
