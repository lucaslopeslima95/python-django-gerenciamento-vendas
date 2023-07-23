from Product.models import Product
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import (LogStoreStock, LogWarehouse, StoreStock,
                     Warehouse, movement_type)


@user_passes_test(lambda user: user.is_superuser or user.is_staff,
                  login_url='user:page_not_found')
@login_required(login_url="login_system")
def stock_management(request):
    storeStock = None
    warehouse = None
    try:
        if 'filter' in request.session:
            filter = request.session['filter']
        else:
            filter = None
        if filter:
            storeStock = StoreStock.objects.filter(
                product__name__startswith=filter).order_by('product')
            request.session['filter'] = ""
        else:
            storeStock = StoreStock.objects.all().order_by('product')
    except Exception as e:
        print(f"Exceção ao listar produtos - {e}")

    return render(request,
                  'stock/stock_management.html',
                  {'storeStock': storeStock,
                   'warehouse': warehouse})


@user_passes_test(lambda user: user.is_superuser or user.is_staff,
                  login_url='user:page_not_found')
@login_required(login_url="login_system")
def stock_management_filter(request):
    try:
        request.session['filter'] = request.GET.get('parametro')
    except Exception as e:
        print(f"Exceção no filtar produto por codigo de barras - {e}")
    return redirect('stock:stock_management')


@user_passes_test(lambda user: user.is_superuser or user.is_staff,
                  login_url='user:page_not_found')
@login_required(login_url="login_system")
def product_movement(request, id):
    try:
        warehouse_quatity, storeStock_quatity = None, None
        product_category, product_selected = None, None

        if request.method == "GET":
            product_selected = Product.objects.get(id=id)
            storeStock_quatity = StoreStock.objects.get(
                product=product_selected).stock_quantity
            warehouse_quatity = Warehouse.objects.get(
                product=product_selected).stock_quantity
            product_category = str(product_selected.category)

    except Exception as e:
        print(f"Exceção lançada ao listar estoques do produto - {e}")

    return render(request, 'stock/product movement.html', {
                                    'product': product_selected,
                                    'product_category': product_category,
                                    'warehouse_quatity': warehouse_quatity,
                                    'storeStock_quatity': storeStock_quatity
                                    })


@user_passes_test(lambda user: user.is_superuser or user.is_staff,
                  login_url='user:page_not_found')
@login_required(login_url="login_system")
def entry_stock(request):
    id_product = request.POST.get('id_product')
    product_quantity = request.POST.get('quantity')

    warehouse = Warehouse.objects.get(product__id=id_product)
    new_quantity = warehouse.stock_quantity + int(product_quantity)

    save_entry_stock_log(request, warehouse)

    warehouse.stock_quantity = new_quantity
    warehouse.save()

    url = f'/stock/product_movement/{id_product}/'

    return redirect(url)


@user_passes_test(lambda user: user.is_superuser or user.is_staff,
                  login_url='user:page_not_found')
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

    transfer_to_store_log(request, warehouse, store_stock, quantity)

    url = f'/stock/product_movement/{id_product}/'
    return redirect(url)


@user_passes_test(lambda user: user.is_superuser or user.is_staff,
                  login_url='user:page_not_found')
@login_required(login_url="login_system")
def manual_destocking(request):
    id_product = request.POST.get('id_product')
    quantity = request.POST.get('quantity')

    store_stock = StoreStock.objects.get(product__id=id_product)
    new_stock_quantity = store_stock.stock_quantity - int(quantity)

    store_stock.stock_quantity = new_stock_quantity
    store_stock.save()

    manual_destocking_log(request,
                          store_stock,
                          quantity)

    url = f'/stock/product_movement/{id_product}/'
    return redirect(url)


def save_entry_stock_log(request, warehouse):
    product_quantity = request.POST.get('quantity')
    LogWarehouse.objects.create(
        product=warehouse.product,
        user=request.user,
        quantity=int(product_quantity),
        type_movement=movement_type.Entrada,
    )


def transfer_to_store_log(request, warehouse, storeStock, quantity):

    LogWarehouse.objects.create(
        product=warehouse.product,
        user=request.user,
        quantity=int(quantity),
        type_movement=movement_type.Transferencia,
    )
    LogStoreStock.objects.create(
        product=storeStock.product,
        user=request.user,
        quantity=int(quantity),
        type_movement=movement_type.Entrada,
    )


def manual_destocking_log(request, storeStock, quantity):
    LogStoreStock.objects.create(
        product=storeStock.product,
        user=request.user,
        quantity=int(quantity),
        type_movement=movement_type.Saida_Manual,
    )


@user_passes_test(lambda user: user.is_superuser or user.is_staff,
                  login_url='user:page_not_found')
@login_required(login_url="login_system")
def show_logs_warehouse(request):
    logsWerehouse = LogWarehouse.objects.all()
    return render(request,
                  'stock/show_logs_warehouse.html',
                  {'logsWerehouse': logsWerehouse})


@user_passes_test(lambda user: user.is_superuser or user.is_staff,
                  login_url='user:page_not_found')
@login_required(login_url="login_system")
def show_logs_store_stock(request):
    logsStoreStock = LogStoreStock.objects.all()
    return render(request,
                  'stock/show_logs_store_stock.html',
                  {'logsStoreStock': logsStoreStock})
