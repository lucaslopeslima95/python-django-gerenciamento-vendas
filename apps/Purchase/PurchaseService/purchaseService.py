import Collaborator
import Purchase
from Purchase.DTO.PurchaseItemDTO import PurchaseItemDTO
from Product.models import Product
from .calculateExpends import (
    calculates_and_returns_current_referral_spending,
    calculates_and_returns_last_reference_spend
    )
from Purchase.models import (
    Purchase,
    PurchaseItem
)
from Collaborator.models import Collaborator
from django.db.models import Sum

class PurchaseService():
    def __init__(self):
      self.purchaseItemDTO = PurchaseItemDTO()
      self.is_start = True
          
    def add_product_to_cart(self,code_bar):
        try:
            product = Product.objects.get(code_bar=code_bar)
            self.purchaseItemDTO.products.append(product)
        except Product.DoesNotExist as e:
            print(f"Produto não encontrado {e}")
            return False
        except Exception as e:
            print(f"Exceção ao buscar o produto pelo codigo de barras no service de purchases - {e}")
            return False
        return True
    
    
    def remove_product_to_cart(self, code_bar):
        try:
            for i,product in self.purchaseItemDTO.products:
                if code_bar == product.code_bar:
                    self.purchaseItemDTO.products.pop(i)
        except ValueError as e:
            print(f"Erro ao remover o produto - {e}")
            return False
        except Exception as e:
            print(f"Exceção ao buscar o produto pelo codigo de barras no service de puchases")
            return False
        return True
    
    def clean_cart(self):
        try:
            self.purchaseItemDTO.products.clear()
        except ValueError as e:
            print(f"Exceção ao limpar ao remover todos os produtos do carrinho - {e}")
            return False
        except Exception as e:
            print(f"Exceção ao remover todos os produtos do carinho {e}")
            return False
        return True
        
    def save_purchase(self,user=None):
        try:
            purchase = Purchase()
            collaborator = Collaborator.objects.get(user=user.id)
            if collaborator.active:
                for productPurchase in self.purchaseItemDTO.products:
                    purchaseItem = PurchaseItem()
                    purchaseItem.product = productPurchase.product
                    purchaseItem.price = productPurchase.price
                    purchaseItem.purchase = purchase
                    purchaseItem.save()
                    Product.objects.filter(id = productPurchase.pk ).update(\
                    stock_quantity=(Product.objects.get(id = productPurchase.pk).stock_quantity-1))
                purchase.save()
                self.checkout(collaborator=collaborator)
            else:
                return False
        
        except Exception as e:
            print(f"Exceção ao salvar a compra {e}")
    
    def checkout(self,collaborator:Collaborator):
        try:
            self.is_start = True
            total_spended = {
                'current':calculates_and_returns_current_referral_spending(collaborator).aggregate(total=Sum('purchaseitem__price'))['total_current'],
                'last': calculates_and_returns_last_reference_spend(collaborator).aggregate(total=Sum('purchaseitem__price'))['total_last'],
                'show_spends':True
                }
            return total_spended
        except Exception as e:
            print(f"Exceção ao fazer o cheout da compra - {e}")
            
