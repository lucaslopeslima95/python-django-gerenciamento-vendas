from django.db import models
from Product.models import Product
from Collaborator.models import Collaborator

class Purchase(models.Model):
    fk_colaborattor = models.ManyToManyField(Collaborator, related_name="purchases", through="PurchaseItems")
    date_purchase = models.DateTimeField(auto_now_add=True)
    
class PurchaseItems(models.Model):
    fk_purchase = models.ForeignKey(Purchase,on_delete=models.CASCADE)
    fk_product = models.ForeignKey(Product,on_delete=models.CASCADE)
    fk_collaborator = models.ForeignKey(Collaborator,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField()
    
    
class deadLine(models.Model):
    DAY = models.IntegerField()