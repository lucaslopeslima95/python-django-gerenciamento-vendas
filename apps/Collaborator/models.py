from django.db import models
from User.models import User

class Collaborator(User):
    cpf = models.CharField(unique=True, max_length=11)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.first_name