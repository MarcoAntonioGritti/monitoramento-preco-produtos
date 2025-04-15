from django.db import models


class Produto(models.Model):
    titulo = models.CharField("TÍTULO DO PRODUTO", max_length=255)
    valor = models.DecimalField("VALOR DO PRODUTO", max_digits=10, decimal_places=2)
    link = models.URLField("LINK PRODUTO", max_length=500, blank=True, null=True)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} | {self.valor} | {self.link} | {self.data}"
