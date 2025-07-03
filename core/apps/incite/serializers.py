# incite/serializers.py (VERSÃO CORRIGIDA E FINAL)

from rest_framework import serializers
from .models import (
    Instituicao,
    Postagem,
    PostagemImagem,
    Pesquisador,
    Pesquisa,
    AcaoExtensionista,
    ProdutoInovacao,
)


# {✪} InstituicaoMarkerSerializer
class InstituicaoMarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instituicao
        fields = [
            "id",
            "nome",
            "cidade_id_mapa",
            "cidade_nome",
            "coordenador_responsavel",
            "email",
            "telefone",
            "informacoes_adicionais",
            "marcador_logo",
            "offset_x",
            "offset_y",
        ]


# (✪) PostagemSerializer - input/output Serializer
class PostagemSerializer(serializers.ModelSerializer):
    """
    Serializer completo para o painel de administração (CRUD de Postagens).
    """

    class Meta:
        model = Postagem
        # ▼▼▼ CAMPOS NOVOS ADICIONADOS AQUI ▼▼▼
        fields = [
            "id",
            "title",
            "content",
            "resumo",
            "imagem_destaque",
            "created_at",
            "updated_at",
            "instituicao",
            "autor",  # <-- Adicionado
        ]
        # O autor será definido automaticamente pela view (perform_create),
        # mas precisa estar nos fields para ser lido.
        read_only_fields = ["created_at", "updated_at"]


# (✪) PostagemBlogSerializer - outputSerializer
class PostagemBlogSerializer(serializers.ModelSerializer):
    """
    Serializer otimizado para a página pública do blog.
    """

    # Para o público, não queremos o ID do autor/instituição, mas sim o nome.
    instituicao_nome = serializers.StringRelatedField(
        source="instituicao", read_only=True, default=""
    )
    autor_nome = serializers.StringRelatedField(source="autor", read_only=True)

    class Meta:
        model = Postagem
        fields = [
            "id",
            "title",
            "resumo",
            "content",
            "imagem_destaque",
            "created_at",
            "instituicao_nome",  # <-- nome em vez do id
            "autor_nome",  # <-- nome em vez do id
        ]


# (✪) PostagemImagemSerializer
class PostagemImagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostagemImagem
        fields = ['id', 'imagem', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at'] # Apenas a imagem é enviada


class PesquisadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pesquisador
        fields = ["id", "nome", "area_atuacao", "desligado", "bolsista", "instituicao"]


class PesquisaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pesquisa
        fields = ["id", "nome", "info", "ano_inicio", "ano_fim", "instituicao"]


class AcaoExtensionistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcaoExtensionista
        fields = ["id", "nome", "info", "ano_inicio", "tipo_comunidade", "instituicao"]


class ProdutoInovacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProdutoInovacao
        fields = ["id", "nome", "info", "ano_inicio", "ano_fim", "instituicao"]


class InstituicaoSerializer(serializers.ModelSerializer):
    # Esta parte, para leitura dos detalhes, permanece a mesma
    postagens = PostagemSerializer(many=True, read_only=True)
    pesquisadores = PesquisadorSerializer(many=True, read_only=True)
    pesquisas = PesquisaSerializer(many=True, read_only=True)
    acoes_extensionistas = AcaoExtensionistaSerializer(many=True, read_only=True)
    produtos = ProdutoInovacaoSerializer(many=True, read_only=True)

    class Meta:
        model = Instituicao
        fields = [
            "id",
            "nome",
            "cidade_id_mapa",
            "cidade_nome",
            "coordenador_responsavel",
            "email",
            "telefone",
            "informacoes_adicionais",
            "offset_x",
            "offset_y",
            "marcador_logo",
            "postagens",
            "pesquisadores",
            "pesquisas",
            "acoes_extensionistas",
            "produtos",
        ]
