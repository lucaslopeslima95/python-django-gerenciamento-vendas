from sqlite3 import IntegrityError

from django.contrib import messages
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import findByNameForm, registerCategoryForm
from .models import Category


@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')     
@login_required(login_url="login_system")
def main_menu_category(request,name=None):
    try:
        form = findByNameForm()
        if not name:
            categorys = Category.objects.all().order_by('name')
        else:
            form = findByNameForm(request.POST)
            categorys = Category.objects.filter(name__startswith=name).order_by('name')
    except (Category.DoesNotExist,Exception) as e:
        print(f"Exceção listar as categorias no menu principal - {e}")
        
    return render(request,'category/main_menu_category.html',{'categorys':categorys,'form':form})

@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')    
@login_required(login_url="login_system")
def save_category(request):
    try:
        if request.method == "POST":
            form = registerCategoryForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name'].capitalize()
                description = form.cleaned_data['description']
                Category.objects.create(name=name,description=description).save()
                messages.success(request, "Salvo com sucesso")
            else:
                messages.warning(request, "Dados Inválidos")
                
            return redirect ('product:main_menu_product')
        else:
         form = registerCategoryForm()
    except (Exception,IntegrityError) as e:
        if 'name' in e:
            messages.warning(request, "Esse nome de categoria ja existe")
        else:
            messages.warning(request, "Erro ao Salvar categoria")
    return render(request, 'category/save_category.html', {'form': form})

@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')      
@login_required(login_url="login_system")
def update_category(request,id):
    form = registerCategoryForm()
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Atualizado com sucesso")
        else:
            messages.warning(request, "Dados Invalido")
            
        return redirect('category:main_menu_category')
    else:
        category_selected = Category.objects.get(id=id)
        form = registerCategoryForm(request.POST or None, instance=category_selected)
        
    return render(request,'product/update_product.html',{'form':form})


     
     
     
