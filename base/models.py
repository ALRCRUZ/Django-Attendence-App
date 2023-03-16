from django.db import models
from django.contrib.auth.models import User



class Presenca(models.Model):
    codigo_adm = models.CharField(max_length=100, null=False, blank=False)
    data_adm = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.codigo_adm


class Aluno(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    codigo_aluno = models.CharField(max_length=100, null=False, blank=False)
    data_aluno = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
