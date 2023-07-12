from Product.models import (
    StoreStock,
    Warehouse
    )

def products_low_stock_StoreStock():
    return StoreStock.objects.filter(stock_quantity__lte=10)

def products_low_stock_Warehouse():
    return Warehouse.objects.filter(stock_quantity__lte=10)
    