from django.db import models
from Product.models import Product
from Collaborator.models import Collaborator

class References(models.IntegerChoices):
        JANEIRO = 1,
        FEVEREIRO = 2,
        MARCO = 3,
        ABRIL = 4,
        MAIO = 5,
        JUNHO = 6,
        JULHO = 7,
        AGOSTO = 8,        
        SETEMBRO = 9,
        OUTUBRO = 10,
        NOVEMBRO = 11,
        DEZEMBRO = 12
        


class Purchase(models.Model):
    fk_product  = models.ManyToManyField(Product,related_name="product",through="Produto_Compra")
	fk_colaborattor = models.ManyToManyField(Collaborator,related_name="collaborator",through="colaborattor_Compra")
	date_puchase

