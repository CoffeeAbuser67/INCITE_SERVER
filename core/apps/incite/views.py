# incite/views.py

from rest_framework import viewsets
from rest_framework.response import Response

from .models import Instituicao, Pesquisador, Pesquisa, Postagem, AcaoExtensionista, ProdutoInovacao
from .serializers import InstituicaoSerializer, PesquisadorSerializer, PesquisaSerializer, PostagemSerializer, AcaoExtensionistaSerializer, ProdutoInovacaoSerializer



class InstituicaoViewSet(viewsets.ModelViewSet):
    queryset = Instituicao.objects.all().order_by('nome')
    serializer_class = InstituicaoSerializer

    def create(self, request, *args, **kwargs):
        # Validação do logo
        logo = request.data.get('marcador_logo')
        if logo:
            # Validação de tamanho (ex: 2MB)
            if logo.size > 2 * 1024 * 1024:
                return Response({'error': 'O logo não pode ter mais de 2MB.'}, status=status.HTTP_400_BAD_REQUEST)
            # Validação de tipo
            if logo.content_type not in ['image/png', 'image/jpeg', 'image/svg+xml']:
                return Response({'error': 'Tipo de arquivo inválido. Use PNG, JPG ou SVG.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().create(request, *args, **kwargs)


    def update(self, request, *args, **kwargs):
        # ... lógica de validação similar ...
        logo = request.data.get('marcador_logo')
        if logo:
            # Validação de tamanho (ex: 2MB)
            if logo.size > 2 * 1024 * 1024:
                return Response({'error': 'O logo não pode ter mais de 2MB.'}, status=status.HTTP_400_BAD_REQUEST)

            # Validação de tipo
            if logo.content_type not in ['image/png', 'image/jpeg', 'image/svg+xml']:
                return Response({'error': 'Tipo de arquivo inválido. Use PNG, JPG ou SVG.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().update(request, *args, **kwargs)








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

    