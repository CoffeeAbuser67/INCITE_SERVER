# incite/views.py

from rest_framework import viewsets, status, permissions, generics
from rest_framework.response import Response

from .models import (
    Instituicao,
    Pesquisador,
    Pesquisa,
    Postagem,
    AcaoExtensionista,
    ProdutoInovacao,
)
from .serializers import (
    InstituicaoSerializer,
    PesquisadorSerializer,
    PesquisaSerializer,
    PostagemSerializer,
    AcaoExtensionistaSerializer,
    ProdutoInovacaoSerializer,
    InstituicaoMarkerSerializer,
    PostagemBlogSerializer,
)

from .permissions import IsPostAuthorOrAdmin


# (✪) InstituicaoViewSet
class InstituicaoViewSet(viewsets.ModelViewSet):
    queryset = Instituicao.objects.all().order_by("nome")
    serializer_class = InstituicaoSerializer
    permission_classes = [permissions.IsAuthenticated]

    # 1. LÓGICA DE PERMISSÃO (QUEM VÊ O QUÊ)
    # (●) get_queryset
    def get_queryset(self):
        """
        - Se o usuário for admin/staff, retorna todas as instituições.
        - Senão, retorna apenas as instituições criadas pelo próprio usuário.
        """
        user = self.request.user
        if user.is_staff:
            return Instituicao.objects.all().order_by("nome")
        return Instituicao.objects.filter(criador=user).order_by("nome")

    # (●) perform_create
    def perform_create(self, serializer):
        # Define automaticamente o usuário logado como o 'criador' ao salvar.
        serializer.save(criador=self.request.user)

    # (●) create
    def create(self, request, *args, **kwargs):
        # Validação do logo
        logo = request.data.get("marcador_logo")
        if logo:
            # Validação de tamanho (2MB)
            if logo.size > 2 * 1024 * 1024:
                return Response(
                    {"error": "O logo não pode ter mais de 2MB."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Validação de tipo
            if logo.content_type not in ["image/png", "image/jpeg", "image/svg+xml"]:
                return Response(
                    {"error": "Tipo de arquivo inválido. Use PNG, JPG ou SVG."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Se a validação passar, chama o método `create` original, que por sua vez
        # chamará "perform_create" para definir o criador.
        return super().create(request, *args, **kwargs)

    # (●) update
    def update(self, request, *args, **kwargs):
        # ... lógica de validação similar ...
        logo = request.data.get("marcador_logo")
        if logo:
            # Validação de tamanho (ex: 2MB)
            if logo.size > 2 * 1024 * 1024:
                return Response(
                    {"error": "O logo não pode ter mais de 2MB."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Validação de tipo
            if logo.content_type not in ["image/png", "image/jpeg", "image/svg+xml"]:
                return Response(
                    {"error": "Tipo de arquivo inválido. Use PNG, JPG ou SVG."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return super().update(request, *args, **kwargs)
# ── ⋙── ── ── ── ── ── ── ──➤


# View Pública 
class PublicInstituicaoDetailView(generics.RetrieveAPIView): # (✪) PublicInstituicaoDetailView
    """
    View pública e somente leitura que retorna os detalhes completos
    de uma única instituição para a página de perfil.
    """
    queryset = Instituicao.objects.all()
    serializer_class = InstituicaoSerializer # Usamos o serializer completo com dados aninhados
    permission_classes = [permissions.AllowAny] # Permite acesso para todos


class InstituicaoMarkerView(generics.ListAPIView):  # ✪ InstituicaoMarkerView
    queryset = Instituicao.objects.all()
    serializer_class = InstituicaoMarkerSerializer
    permission_classes = [permissions.AllowAny]


class PesquisadorViewSet(viewsets.ModelViewSet):  # ✪ PesquisadorViewSet
    queryset = Pesquisador.objects.all()
    serializer_class = PesquisadorSerializer


class PesquisaViewSet(viewsets.ModelViewSet):  # ✪ PesquisaViewSet
    queryset = Pesquisa.objects.all()
    serializer_class = PesquisaSerializer


class PostagemViewSet(viewsets.ModelViewSet):  # (✪) PostagemViewSet
    queryset = Postagem.objects.all()
    serializer_class = PostagemSerializer
    permission_classes = [permissions.IsAuthenticated, IsPostAuthorOrAdmin]

    def get_queryset(self):
        """
        NOTE
        Filtra o queryset de postagens.
        -» Admins podem ver tudo.
        -» Usuários básicos só veem posts de suas instituições.
        -» Aceita um query param `?tipo=geral` para filtrar apenas posts sem instituição.
        """
        user = self.request.user

        # Começa com o queryset base
        if user.is_staff:
            queryset = Postagem.objects.all()
        else:
            # Filtra por instituições que o usuário criou
            queryset = Postagem.objects.filter(instituicao__criador=user)

        """
        NOTE
        -» As calls provenientes do form de PostsGerais dinamicamente adicionam o parametro tipo no request 
        -» fetchPostsGerais add o param tipo com value = geral.
        -» const response = await axiosForInterceptor.get('/postagens/?tipo=geral');
        """

        tipo_filtro = self.request.query_params.get("tipo")
        if tipo_filtro == "geral":
            # Se o filtro 'geral' for solicitado, retorna apenas posts onde a instituição é nula
            return queryset.filter(instituicao__isnull=True).order_by("-created_at")

        return queryset.order_by("-created_at")

    def perform_create(self, serializer):
        # Associa o autor logado, a instituição virá (ou não) do payload
        serializer.save(autor=self.request.user)

# Viewset Público
class PostagemBlogViewSet(viewsets.ReadOnlyModelViewSet): # (✪) PostagemBlogViewSet
    queryset = Postagem.objects.all().order_by("-created_at")
    serializer_class = PostagemBlogSerializer
    permission_classes = [permissions.AllowAny]


class AcaoExtensionistaViewSet(viewsets.ModelViewSet):  # ✪ AcaoExtensionistaViewSet
    queryset = AcaoExtensionista.objects.all()
    serializer_class = AcaoExtensionistaSerializer


class ProdutoInovacaoViewSet(viewsets.ModelViewSet):  # ✪ ProdutoInovacaoViewSet
    queryset = ProdutoInovacao.objects.all()
    serializer_class = ProdutoInovacaoSerializer
