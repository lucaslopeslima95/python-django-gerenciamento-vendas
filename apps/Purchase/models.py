from django.db import models
from Product.models import Product
from Collaborator.models import Collaborator

class Purchase(models.Model):
    collaborator = models.ForeignKey(Collaborator,on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, related_name="purchases", through="PurchaseItem")
    date_purchase = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Compra do Colaborador {str(self.collaborator)}"
    
class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    def __str__(self):
        return str(self.product)
    
    
class DeadLine(models.Model):
    DAY = models.IntegerField()
    def __str__(self):
        return str(self.DAY)