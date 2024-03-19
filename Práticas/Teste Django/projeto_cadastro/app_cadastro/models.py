from django.db import models

class Usuario(models.Model):

    id = models.AutoField(primary_key=True)

    nome = models.TextField(max_length=255)

    idade = models.IntegerField()

