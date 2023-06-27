from django.db import models
from User.models import User

class Collaborator(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=255,default="Nome Teste")
    cpf = models.CharField(unique=True, max_length=14,default="999.999.999-99")
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.name