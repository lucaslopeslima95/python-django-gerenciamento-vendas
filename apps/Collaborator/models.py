from django.db import models
from User.models import User

class Collaborator(models.Model):
    id_collaborator = models.AutoField(primary_key=True)
    user_fk = models.OneToOneField(User,on_delete=models.CASCADE)
    cpf = models.CharField(unique=True, max_length=11)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.first_name