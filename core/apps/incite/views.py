# incite/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Instituicao, Pesquisador, Pesquisa, Postagem, AcaoExtensionista, ProdutoInovacao
from .serializers import InstituicaoSerializer, PesquisadorSerializer, PesquisaSerializer, PostagemSerializer, AcaoExtensionistaSerializer, ProdutoInovacaoSerializer



# ✪ InstituicaoViewSet
class InstituicaoViewSet(viewsets.ModelViewSet):
    queryset = Instituicao.objects.all().order_by('nome')
    serializer_class = InstituicaoSerializer

    # 1. LÓGICA DE PERMISSÃO (QUEM VÊ O QUÊ)
    # ● get_queryset
    def get_queryset(self):

        """
        - Se o usuário for admin/staff, retorna todas as instituições.
        - Senão, retorna apenas as instituições criadas pelo próprio usuário.
        """
        user = self.request.user
        if user.is_staff:
            return Instituicao.objects.all().order_by('nome')
        return Instituicao.objects.filter(criador=user).order_by('nome')

    # ● perform_create
    def perform_create(self, serializer):
        # Define automaticamente o usuário logado como o 'criador' ao salvar.
        serializer.save(criador=self.request.user)


    # ● create
    def create(self, request, *args, **kwargs):
        # Validação do logo
        logo = request.data.get('marcador_logo')
        if logo:

            # Validação de tamanho (2MB)
            if logo.size > 2 * 1024 * 1024:
                return Response({'error': 'O logo não pode ter mais de 2MB.'}, status=status.HTTP_400_BAD_REQUEST)
            # Validação de tipo
            if logo.content_type not in ['image/png', 'image/jpeg', 'image/svg+xml']:
                return Response({'error': 'Tipo de arquivo inválido. Use PNG, JPG ou SVG.'}, status=status.HTTP_400_BAD_REQUEST)
        

        # Se a validação passar, chama o método `create` original, que por sua vez
        # chamará "perform_create" para definir o criador.
        return super().create(request, *args, **kwargs)

    # ● update
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
# ── ⋙── ── ── ── ── ── ── ──➤


class PesquisadorViewSet(viewsets.ModelViewSet): # ✪ PesquisadorViewSet
    queryset = Pesquisador.objects.all()
    serializer_class = PesquisadorSerializer

class PesquisaViewSet(viewsets.ModelViewSet): # ✪ PesquisaViewSet
    queryset = Pesquisa.objects.all()
    serializer_class = PesquisaSerializer

class PostagemViewSet(viewsets.ModelViewSet): # ✪ PostagemViewSet
    queryset = Postagem.objects.all()
    serializer_class = PostagemSerializer

class AcaoExtensionistaViewSet(viewsets.ModelViewSet): # ✪ AcaoExtensionistaViewSet
    queryset = AcaoExtensionista.objects.all()
    serializer_class = AcaoExtensionistaSerializer

class ProdutoInovacaoViewSet(viewsets.ModelViewSet): # ✪ ProdutoInovacaoViewSet
    queryset = ProdutoInovacao.objects.all()
    serializer_class = ProdutoInovacaoSerializer

    