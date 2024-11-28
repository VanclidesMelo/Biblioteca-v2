from django.db import models
from django.contrib.auth.models import User, AbstractUser


class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Autor(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    publicado_em = models.DateField()

    def __str__(self):
        return self.titulo


class Colecao(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    livros = models.ManyToManyField(Livro, related_name="colecoes")
    colecionador = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="colecoes")

    def __str__(self):
        return f"{self.nome} - {self.colecionador.username}"


class Usuario(AbstractUser):
    # Garante unicidade no email
    email = models.EmailField(unique=True, verbose_name="Email")
    nome_completo = models.CharField(
        max_length=150, verbose_name="Nome completo", blank=True, null=True)
    bio = models.TextField(verbose_name="Biografia", blank=True, null=True)

    # Campo adicional opcional: avatar do usuário
    avatar = models.ImageField(
        upload_to="avatars/", verbose_name="Avatar", blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
