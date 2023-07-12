from django.db import models
from Category.models import Category
from User.models import User

    
class movement_type(models.IntegerChoices):
        Entrada = 1,
        Saida = 2,
        Transferencia = 3,
        Saida_Manual = 4
      

class Product(models.Model):
    name = models.CharField(max_length=50,unique=True)
    code_bar = models.CharField(max_length=16,unique=True)
    price = models.DecimalField(decimal_places=2,max_digits=5)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category,on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.name

class StoreStock(models.Model):
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    stock_quantity = models.IntegerField(default=0)
    def __str__(self):
        return str(self.product)

class Warehouse(models.Model):
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    stock_quantity = models.IntegerField(default=0)
    def __str__(self):
        return str(self.product)


class LogStoreStock(models.Model):
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=0)
    type_movement = models.IntegerField(default=movement_type.Entrada ,choices=movement_type.choices)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.type_movement)
    
class LogWarehouse(models.Model):
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=0)
    type_movement = models.IntegerField(default=movement_type.Entrada ,choices=movement_type.choices)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.type_movement)
