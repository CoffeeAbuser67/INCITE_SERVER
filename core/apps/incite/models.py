from django.conf import settings
from django.db import models


# 🧿
# {✪} Instituicao
class Instituicao(models.Model):
    # Campos obrigatórios
    nome = models.CharField(max_length=255)
    cidade_id_mapa = models.CharField(
        max_length=100, db_index=True, null=True, blank=True
    )

    cidade_nome = models.CharField(max_length=150, null=True, blank=True)

    coordenador_responsavel = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)

    # ForeignKey para o modelo de usuário que definimos em settings.py
    # WARN Nao pode ter blank nem null= True
    criador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="instituicoes",
        blank=True,
        null=True,
    )

    marcador_logo = models.ImageField(
        upload_to="logos_instituicoes/", blank=True, null=True
    )
    offset_x = models.FloatField(default=0)
    offset_y = models.FloatField(default=0)

    # Campos opcionais
    quantidade_pesquisadores = models.PositiveIntegerField(default=0)
    informacoes_adicionais = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome


#  . . .


# ✪ Pesquisador
class Pesquisador(models.Model):
    instituicao = models.ForeignKey(
        Instituicao, related_name="pesquisadores", on_delete=models.CASCADE
    )
    nome = models.CharField(max_length=255)
    area_atuacao = models.CharField(max_length=255, blank=True, null=True)
    desligado = models.BooleanField(default=False)
    bolsista = models.BooleanField(default=False)

    def __str__(self):
        return self.nome


# ✪ Pesquisa
class Pesquisa(models.Model):
    instituicao = models.ForeignKey(
        Instituicao, related_name="pesquisas", on_delete=models.CASCADE
    )
    nome = models.CharField(max_length=255)
    info = models.TextField()
    ano_inicio = models.PositiveIntegerField()
    ano_fim = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.nome


# ✪ AcaoExtensionista
class AcaoExtensionista(models.Model):
    COMUNIDADE_CHOICES = [
        ("TR", "Tradicionais"),
        ("IN", "Indígenas"),
        ("QU", "Quilombolas"),
        ("AS", "Assentamentos"),
    ]
    instituicao = models.ForeignKey(
        Instituicao, related_name="acoes_extensionistas", on_delete=models.CASCADE
    )
    nome = models.CharField(max_length=255)
    info = models.TextField()
    ano_inicio = models.PositiveIntegerField()
    ano_fim = models.PositiveIntegerField(blank=True, null=True)
    tipo_comunidade = models.CharField(
        max_length=2, choices=COMUNIDADE_CHOICES, blank=True, null=True
    )

    def __str__(self):
        return self.nome


# ✪ ProdutoInovacao
class ProdutoInovacao(models.Model):
    instituicao = models.ForeignKey(
        Instituicao, related_name="produtos", on_delete=models.CASCADE
    )
    nome = models.CharField(max_length=255)
    info = models.TextField()
    ano_inicio = models.PositiveIntegerField()
    ano_fim = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.nome


# ✪ Postagem
class Postagem(models.Model):
    instituicao = models.ForeignKey(
        Instituicao,
        related_name="postagens",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="postagens_criadas",
    )
    resumo = models.CharField(max_length=400, blank=True, null=True)
    imagem_destaque = models.ImageField(upload_to="post_images/", blank=True, null=True)

    title = models.CharField(max_length=255)
    content = models.TextField()  # Aqui será salvo o HTML do nosso editor!
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
