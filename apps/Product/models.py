from django.db import models
from Category.models import Category


class status_type(models.IntegerChoices):
    Ativo = 1,
    Inativo = 2


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code_bar = models.CharField(max_length=16, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    active = models.IntegerField(
        default=status_type.Ativo, choices=status_type.choices)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name
