from django.db import models


class Caso(models.Model):
    STATUS = [("desaparecido", "Desaparecido(a)"), ("encontrado", "Encontrado(a)")]

    nome = models.CharField(max_length=150)
    idade = models.PositiveIntegerField()
    foto = models.ImageField(upload_to="fotos/")
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2, default="RJ")
    data_desaparecimento = models.DateField("data do desaparecimento")
    descricao = models.TextField("descrição")
    contato = models.CharField("contato da família", max_length=100)
    numero_bo = models.CharField("número do B.O.", max_length=50)
    status = models.CharField(max_length=20, choices=STATUS, default="desaparecido")
    aprovado = models.BooleanField(default=False)
    data_encontrado = models.DateField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.nome} ({self.cidade})"
