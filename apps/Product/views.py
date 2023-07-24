from django.contrib import messages
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import redirect, render
from Stock.models import StoreStock, Warehouse

from .forms import registerProductForm
from .models import Product


@user_passes_test(lambda user: user.is_superuser or user.is_staff,
                  login_url='user:page_not_found')
@login_required(login_url="login_system")
def main_menu_product(request):
    try:
        if 'filter' in request.session:
            filter = request.session['filter']
        else:
            filter = None
        if filter:
            products = Product.objects.filter(
                name__startswith=filter).order_by('active')
            request.session['filter'] = ""
        else:
            products = Product.objects.all().order_by('active')
    except Exception as e:
        print(f"Exceção ao listar produtos - {e}")
    return render(request, 'product/main_menu_product.html',
                  {'products': products})


@user_passes_test(lambda user: user.is_superuser or user.is_staff,
                  login_url='user:page_not_found')
@login_required(login_url="login_system")
def save_product(request):
    try:
        if request.method == "POST":
            form = registerProductForm(request.POST)
            if form.is_valid():
                code_bar_masked = form.cleaned_data['code_bar']
                code_bar = code_bar_masked.\
                    replace("-", "").replace("-", "").replace("-", "")
                name = form.cleaned_data['name']
                price = form.cleaned_data['price']
                category = form.cleaned_data['category']
                Product.objects.create(code_bar=code_bar,
                                       name=name,
                                       price=price,
                                       category=category).save()
                messages.success(request, "Salvo com sucesso")
                return redirect('product:main_menu_product')
        else:
            form = registerProductForm()
    except Exception as e:
        print(f"Codigo de Barras ja existe -  {e}")
        messages.warning(request, "Codigo de Barras ja existe")
    return render(request, 'product/save_product.html', {'form': form})


@receiver(post_save, sender=Product)
def create_stocks(sender, instance, created, **kwargs):
    try:
        if created:
            StoreStock.objects.create(product=instance).save()
            Warehouse.objects.create(product=instance).save()
    except Exception as e:
        print(f"Exceção instancias de storestock e warehouse - {e}")


@user_passes_test(lambda user: user.is_superuser or user.is_staff,
                  login_url='user:page_not_found')
@login_required(login_url="login_system")
def deactivate_product(request, id):
    try:
        Product.objects.filter(id=id).update(
            active=not Product.objects.get(id=id).active)
    except Exception as e:
        print(f"Exceção no excluir produto {e}")
    return redirect('product:main_menu_product')


@user_passes_test(lambda user: user.is_superuser or user.is_staff,
                  login_url='user:page_not_found')
@login_required(login_url="login_system")
def update_product(request, id):
    try:
        form = None
        product_chosen = Product.objects.get(id=id)
        product_chosen.price = (
            f"R$ {str(product_chosen.price).replace('.', ',')}")
        form = registerProductForm(request.POST or None,
                                   instance=product_chosen)
        if request.method == "POST":
            if form.is_valid():
                code_bar_masked = form.cleaned_data['code_bar']
                code_bar = code_bar_masked.\
                    replace("-", "").replace("-", "").replace("-", "")
                name = form.cleaned_data['name']
                price = form.cleaned_data['price']
                category = form.cleaned_data['category']
                active = form.cleaned_data['active']
                Product.objects.filter(code_bar=code_bar).update(
                                       name=name,
                                       price=price,
                                       category=category,
                                       code_bar=code_bar,
                                       active=active
                                    )
                messages.success(request, "Atualizado com sucesso")
                return redirect('product:main_menu_product')
            else:
                messages.warning(request, "Dados Invalido")
    except Exception as e:
        print(f"Exceção lançada ao salvar a atualização do produto  -  {e}")
        messages.warning(request, "Codigo de Barras ja existe")
        
    return render(request, 'product/update_product.html', {'form': form})


@user_passes_test(lambda user: user.is_superuser or user.is_staff,
                  login_url='user:page_not_found')
@login_required(login_url="login_system")
def update_status_product(request, id):
    try:
        Product.objects.filter(id=id).update(
            active=not Product.objects.get(id=id).active)
    except Exception as e:
        print(f"Exceção ao atualizar a situação do produto - {e}")
    return redirect('stock:stock_management')
