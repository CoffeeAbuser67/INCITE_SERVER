# incite/views.py

from rest_framework import viewsets
from .models import Instituicao, Pesquisador, Pesquisa, Postagem, AcaoExtensionista, ProdutoInovacao
from .serializers import InstituicaoSerializer, PesquisadorSerializer, PesquisaSerializer, PostagemSerializer, AcaoExtensionistaSerializer, ProdutoInovacaoSerializer

class InstituicaoViewSet(viewsets.ModelViewSet):
    queryset = Instituicao.objects.all().order_by('nome')
    serializer_class = InstituicaoSerializer

class PesquisadorViewSet(viewsets.ModelViewSet):
    queryset = Pesquisador.objects.all()
    serializer_class = PesquisadorSerializer

class PesquisaViewSet(viewsets.ModelViewSet):
    queryset = Pesquisa.objects.all()
    serializer_class = PesquisaSerializer

class PostagemViewSet(viewsets.ModelViewSet):
    queryset = Postagem.objects.all()
    serializer_class = PostagemSerializer

# ▼▼▼ CORREÇÃO E ADIÇÃO AQUI ▼▼▼
class AcaoExtensionistaViewSet(viewsets.ModelViewSet): # Nome da classe corrigido
    queryset = AcaoExtensionista.objects.all()
    serializer_class = AcaoExtensionistaSerializer

class ProdutoInovacaoViewSet(viewsets.ModelViewSet): # Nome da classe corrigido
    queryset = ProdutoInovacao.objects.all()
    serializer_class = ProdutoInovacaoSerializer

    