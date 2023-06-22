from Product.models import Product
from decimal import Decimal

class PurchaseItemDTO:
    def __init__(self):
        self._product: Product
        self._price: float
        self._quantity: int
        self._total_cost: float
        
    @property
    def product(self):
        return self._product
    
    @product.setter
    def product(self, new_product):
        if isinstance(new_product, Product):
            self._product = new_product
        else:
            raise Exception("Purchase DTO - Exceção de instância de produto")
    
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, new_price):
        if isinstance(new_price,Decimal):
            self._price = new_price
        else:
            raise Exception(" - Tipo de Preço Incompatível")
    
    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, new_quantity):
        if isinstance(new_quantity, int):
            self._quantity = new_quantity
        else:
            raise Exception("Tipo de Quantidade Incompatível")
   
    @property
    def total_cost(self):
        return self._total_cost
    
    @total_cost.setter
    def total_cost(self, new_total_cost):
        if isinstance(new_total_cost, Decimal):
            self._total_cost = new_total_cost
        else:
            raise Exception("Tipo de Preço Total Incompatível")

