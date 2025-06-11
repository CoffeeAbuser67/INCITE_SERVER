# incite/serializers.py (VERSÃO CORRIGIDA E FINAL)

from rest_framework import serializers
from .models import Instituicao, Postagem, Pesquisador, Pesquisa, AcaoExtensionista, ProdutoInovacao

class PostagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postagem
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'instituicao']
        read_only_fields = ['created_at', 'updated_at']

class PesquisadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pesquisador
        fields = ['id', 'nome', 'area_atuacao', 'desligado', 'bolsista', 'instituicao']

class PesquisaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pesquisa
        fields = ['id', 'nome', 'info', 'ano_inicio', 'ano_fim', 'instituicao']

class AcaoExtensionistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcaoExtensionista
        fields = ['id', 'nome', 'info', 'ano_inicio', 'tipo_comunidade', 'instituicao']

class ProdutoInovacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProdutoInovacao
        fields = ['id', 'nome', 'info', 'ano_inicio', 'ano_fim', 'instituicao']


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
            'id', 'nome', 'cidade', 'coordenador_responsavel', 'email', 'telefone', 
            'informacoes_adicionais', 'postagens', 'pesquisadores', 'pesquisas', 
            'acoes_extensionistas', 'produtos'
        ]