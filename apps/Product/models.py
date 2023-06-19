from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=50,unique=True)
    code_bar = models.CharField(max_length=14,unique=True)
    price = models.DecimalField(decimal_places=2,max_digits=5)
    stock_quantity = models.IntegerField()
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return self.name

