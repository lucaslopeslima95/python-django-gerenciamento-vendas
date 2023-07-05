from Product.models import Product
def products_low_stock():
    return Product.objects.filter(stock_quantity__lte=10)