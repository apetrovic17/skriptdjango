from django.db import models
from django.contrib.auth.models import User

class Patike(models.Model):
    naziv=models.CharField(max_length=64,default='')
    model = models.CharField(max_length=64, default='')
    velicina = models.IntegerField(default=0)
    cena = models.IntegerField(default=0)


    def __str__(self):
        return self.naziv + ' ' +self.model


class Ocene(models.Model):
    ocena = models.IntegerField(default=0)
    opis = models.CharField(max_length=64, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    patike = models.ForeignKey(Patike, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.opis

