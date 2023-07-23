from django.db import models
from User.models import User


class status_collaborator(models.IntegerChoices):
    Ativo = 1,
    Inativo = 2


class Collaborator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="Nome Teste")
    cpf = models.CharField(unique=True, max_length=14,
                           default="999.999.999-99")
    active = models.IntegerField(default=status_collaborator.Ativo,
                                 choices=status_collaborator.choices)

    def __str__(self):
        return self.name
