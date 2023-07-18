from django.contrib import messages
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.db.models.signals import post_save
from django.dispatch import receiver


from .forms import registerProductForm
from .models import LogStoreStock, LogWarehouse, Product, StoreStock, Warehouse, movement_type



@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')     
@login_required(login_url="login_system")
def main_menu_product(request):
    """
    Exibe o menu principal de produtos.

    Args:
        request: O objeto de requisição HTTP.

    Returns:
        Um objeto de resposta HTTP renderizando o template 'product/main_menu_product.html' com os produtos a serem exibidos.

    Raises:
        None
    """
    try:
        if 'filter' in request.session:
            filter = request.session['filter']
        else:
            filter = None
        if filter:
            products = Product.objects.filter(name__startswith=filter).order_by('active')
            request.session['filter'] = ""
        else:
            products = Product.objects.all().order_by('active')
    except Exception as e:
        print(f"Exceção ao listar produtos - {e}")
        
    return render(request,'product/main_menu_product.html',{'products':products})

@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')    
@login_required(login_url="login_system")
def save_product(request):
    try:
        if request.method == "POST":
            form = registerProductForm(request.POST)
            if form.is_valid():
                code_bar_with_mask = form.cleaned_data['code_bar']
                code_bar = code_bar_with_mask.replace("-","").replace("-","").replace("-","")
                name =  form.cleaned_data['name']
                price = form.cleaned_data['price']
                category = form.cleaned_data['category']
                Product.objects.create(code_bar=code_bar,name=name,price=price,category=category).save()
                messages.success(request, "Salvo com sucesso")
                return redirect ('product:main_menu_product')
        else:
         form = registerProductForm()
    except Exception as e:
        print(f"Codigo de Barras ja existe {e}")
        messages.warning(request, "Codigo de Barras ja existe")
    return render(request, 'product/save_product.html', {'form': form})

@receiver(post_save, sender=Product)
def create_stocks(sender, instance, created, **kwargs):
    """
    Cria objetos StoreStock e Warehouse após salvar um produto.

    Args:
        sender: A classe de modelo que enviou o sinal (Product).
        instance: A instância do modelo Product que foi salva.
        created: Um valor booleano indicando se a instância do modelo foi criada ou atualizada.
    """
    try:
        if created:
            StoreStock.objects.create(product=instance).save()
            Warehouse.objects.create(product=instance).save()
    except Exception as e:
        print(f"Exceção lançada ao criar instancias de storestock e warehouse - {e}")


@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')        
@login_required(login_url="login_system")
def deactivate_product(request, id):
    try:
        Product.objects.filter(id=id).update(active = not Product.objects.get(id=id).active)
    except Exception as e:
        print(f"Exceção no excluir produto {e}")
    return redirect('product:main_menu_product')

@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')      
@login_required(login_url="login_system")
def update_product(request,id):
    try:
        product_selected = Product.objects.get(id=id)
        form = registerProductForm(request.POST or None, instance=product_selected)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Atualizado com sucesso")
                return redirect('product:main_menu_product')
            else:
                messages.warning(request, "Dados Invalido")
    except Exception as e:
        print(f"Exceção lançada ao salvar a atualização do produto  -  {e}")        
    return render(request,'product/update_product.html',{'form':form})

@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')    
@login_required(login_url="login_system")
def main_menu_product_with_filter(request):
    try:
        request.session['filter'] = request.GET.get('parametro')
    except Exception as e:
        print(f"Exceção no filtar produco por codigo de barras - {e}")
    return redirect('product:main_menu_product')
        

@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')    
@login_required(login_url="login_system")
def update_status_product(request,id):
    try:
        Product.objects.filter(id=id).update(active = not Product.objects.get(id=id).active)
    except Exception as e:
        print(f"Exceção ao atualizar a situação do produto - {e}")
    return redirect('product:stock_management')

@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')    
@login_required(login_url="login_system")
def stock_management(request):
    storeStock = None
    warehouse  = None
    try:
        if 'filter' in request.session:
            filter = request.session['filter']
        else:
            filter = None
        if filter:
            storeStock = StoreStock.objects.filter(product__name__startswith=filter).order_by('product')
            request.session['filter'] = ""
        else:
            storeStock = StoreStock.objects.all().order_by('product')
    except Exception as e:
        print(f"Exceção ao listar produtos - {e}")
        
    return render(request,'product/stock_management.html',{'storeStock':storeStock,'warehouse':warehouse})


@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')    
@login_required(login_url="login_system")
def stock_management_filter(request):
    try:
        request.session['filter'] = request.GET.get('parametro')
    except Exception as e:
        print(f"Exceção no filtar produto por codigo de barras - {e}")
    return redirect('product:stock_management')
 
 
@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')    
@login_required(login_url="login_system")  
def product_movement(request,id):
    try:

        warehouse_quatity,storeStock_quatity = None, None
        product_category,product_selected = None, None
        if request.method == "GET":
            
            product_selected = Product.objects.get(id=id)
            storeStock_quatity = StoreStock.objects.get(product=product_selected).stock_quantity
            warehouse_quatity = Warehouse.objects.get(product=product_selected).stock_quantity
            product_category = str(product_selected.category)
    except Exception as e:
        print(f"Exceção lançada ao listar estoques do produto -  {e}")
    
    return render(request,'product/product movement.html',{
                                                           'product':product_selected,
                                                           'product_category':product_category,
                                                           'warehouse_quatity':warehouse_quatity,
                                                           'storeStock_quatity':storeStock_quatity
                                                          })
    
    
@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')    
@login_required(login_url="login_system")  
def entry_stock(request):
    id_product = request.POST.get('id_product')
    product_quantity = request.POST.get('quantity')

    warehouse = Warehouse.objects.get(product__id=id_product)
    new_warehouse_stock_quantity = warehouse.stock_quantity + int(product_quantity)

    save_entry_stock_log(request, warehouse)
    
    warehouse.stock_quantity = new_warehouse_stock_quantity
    warehouse.save()

    
    url = f'/product/product_movement/{id_product}/'
    
    return redirect(url)


@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')    
@login_required(login_url="login_system")  
def transfer_to_store(request):
    id_product = request.POST.get('id_product')
    quantity = request.POST.get('quantity')
    
    warehouse = Warehouse.objects.get(product__id=id_product)
    new_warehouse_stock_quantity = warehouse.stock_quantity - int(quantity)
    warehouse.stock_quantity = new_warehouse_stock_quantity
    warehouse.save()
    
    store_stock = StoreStock.objects.get(product__id=id_product)
    new_store_stock_quantity = store_stock.stock_quantity + int(quantity)
    store_stock.stock_quantity = new_store_stock_quantity
    store_stock.save()

    transfer_to_store_log(request,warehouse,store_stock,quantity)
    
    url = f'/product/product_movement/{id_product}/'
    return redirect(url)


@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')    
@login_required(login_url="login_system")  
def manual_destocking(request):
    id_product = request.POST.get('id_product')
    quantity = request.POST.get('quantity')
    
    store_stock = StoreStock.objects.get(product__id=id_product)
    new_stock_quantity = store_stock.stock_quantity - int(quantity)

    store_stock.stock_quantity = new_stock_quantity
    store_stock.save()
    
    manual_destocking_log(request,store_stock,quantity)
    
    url = f'/product/product_movement/{id_product}/'
    return redirect(url)


def save_entry_stock_log(request,warehouse):
    product_quantity = request.POST.get('quantity')
    LogWarehouse.objects.create(
        product = warehouse.product,
        user = request.user,
        quantity = int(product_quantity),
        type_movement=movement_type.Entrada,
    )

def transfer_to_store_log(request,warehouse,storeStock,quantity):    
   
    LogWarehouse.objects.create(
        product = warehouse.product,
        user = request.user,
        quantity = int(quantity),
        type_movement=movement_type.Transferencia,
    )
    LogStoreStock.objects.create(
        product = storeStock.product,
        user = request.user,
        quantity = int(quantity),
        type_movement=movement_type.Entrada,
    )
    
def manual_destocking_log(request,storeStock,quantity):
    LogStoreStock.objects.create(
        product = storeStock.product,
        user = request.user,
        quantity = int(quantity),
        type_movement=movement_type.Saida_Manual,
    )
    
    
@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')    
@login_required(login_url="login_system")      
def show_logs_warehouse(request):
    logsWerehouse = LogWarehouse.objects.all()
    return render(request, 'product/show_logs_warehouse.html',{'logsWerehouse':logsWerehouse})

    
@user_passes_test(lambda user: user.is_superuser or user.is_staff,login_url='user:page_not_found')    
@login_required(login_url="login_system")      
def show_logs_store_stock(request):
    logsStoreStock = LogStoreStock.objects.all()
    return render(request, 'product/show_logs_store_stock.html',{'logsStoreStock':logsStoreStock})


