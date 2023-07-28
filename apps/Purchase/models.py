from django.db import models
from Product.models import Product
from Collaborator.models import Collaborator


class Purchase(models.Model):
    collaborator = models.ForeignKey(Collaborator, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, related_name="purchases",
                                     through="PurchaseItem")
    date_purchase = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Compra do Colaborador {str(self.collaborator)}"


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return str(self.product)


class DeadLine(models.Model):
    DAY = models.IntegerField()

    def __str__(self):
        return str(self.DAY)


class info_utils(models.Model):
    email_marketing = models.CharField(max_length=50)
    email_rh = models.CharField(max_length=50)

    def __str__(self):
        return f"RH: {self.email_rh},   Marketing: {self.email_marketing}"


class SmtpConfiguration(models.Model):
    host = models.CharField(max_length=100)
    port = models.PositiveIntegerField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    use_tls = models.BooleanField(default=True)

    def __str__(self):
        return self.host
