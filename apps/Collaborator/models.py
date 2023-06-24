from django.db import models

class Collaborator(models.Model):
    username = models.CharField(unique=True, max_length=20,default="User Teste")
    name = models.CharField(max_length=20,default="Nome Teste")
    cpf = models.CharField(unique=True, max_length=14,default="999.999.999-99")
    email = models.EmailField(default="teste@teste.com")
    password = models.CharField(max_length=20,default="1111111111")
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.username