from dj_rest_auth.views import PasswordResetConfirmView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import permissions

from apps.agricultura.views import TOPValuesView, TopTimeSeriesView, RegionValuesView
from apps.cache.views import Temp_cache_view
from rest_framework.routers import DefaultRouter

from allauth.account.views import ConfirmEmailView

from apps.users.views import UserViewSet 

from apps.incite.views import (
    InstituicaoMarkerView,
    InstituicaoViewSet, 
    PesquisadorViewSet, 
    PesquisaViewSet,
    PostagemViewSet,
    PostagemBlogViewSet,
    AcaoExtensionistaViewSet,
    ProdutoInovacaoViewSet,
    PublicInstituicaoDetailView,
    PostagemImagemUploadView,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'instituicoes', InstituicaoViewSet)
router.register(r'pesquisadores', PesquisadorViewSet)
router.register(r'pesquisas', PesquisaViewSet) # Você já tinha o ViewSet, só faltava registrar
router.register(r'postagens', PostagemViewSet)
router.register(r'blog/posts', PostagemBlogViewSet, basename='blog-post') 
router.register(r'acoes_extensionistas', AcaoExtensionistaViewSet)
router.register(r'produtos', ProdutoInovacaoViewSet)


urlpatterns = [

    path(settings.ADMIN_URL, admin.site.urls),
    
    # ★ ── ⋙⇌⇌⇌⇌⇌⇌⇌⇌⇌⇌⇌⇌⇌⇌⇌⫸
    # ★ df-rest-auth 🛡️
    # ★ ── ⋙⇌⇌⇌⇌⇌⇌⇌⇌⇌⇌⇌⇌⇌⇌⇌⫸

    path("api/v1/auth/", include("dj_rest_auth.urls")),
    # [ROUTE]  api/v1/auth/password/reset/?$
    # [ROUTE]  api/v1/auth/password/reset/confirm/?$'
    # [ROUTE]  api/v1/auth/login/?$
    # [ROUTE]  api/v1/auth/logout/?$
    # [ROUTE]  api/v1/auth/user/?$
    # [ROUTE]  api/v1/auth/password/change/?$
    # [ROUTE]  api/v1/auth/token/refresh/
    # [ROUTE]  api/v1/auth/token/verify/

    # . . . . . 
    re_path(
        r"^api/v1/auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$",
        ConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
    # [ROUTE]  api/v1/auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$
    # NOTE  registration/account-confirm-email must be on top of dj_rest_auth.registration.urls
    # . . . . . 
    
    path("api/v1/auth/registration/", include("dj_rest_auth.registration.urls")),
    # [ROUTE]  api/v1/auth/registration/''
    # [ROUTE]  api/v1/auth/verify-email/?$
    # [ROUTE]  api/v1/auth/resend-email/?$
    # [ROUTE]  api/v1/auth/account-email-verification-sent/?$
    path(
        "api/v1/auth/password/reset/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    # [ROUTE] api/v1/auth/password/reset/confirm/<uidb64>/<token>/


    # ── ◯─◡◠◡◠◡ USERS + INSTITUIÇÕES + PESQUISADORES + POSTAGENS & ETC ◠◡◠◡◠◡◠◡◠─➤
    # . . . 🔒
    path('api/v1/', include(router.urls)),
    # [ROUTE]  api/v1/users/
    # [ROUTE]  api/v1/users/{id}/ 
    # [ROUTE]  api/v1/users/
    # [ROUTE]  api/v1/users/{id}/ 
    # [ROUTE]  api/v1/users/
    # [ROUTE]  api/v1/users/{id}/ 

    # . . . 🔒

    # [ROUTE]  api/v1/instituicoes/
    # [ROUTE]  api/v1/instituicoes/{id}/ 
    # [ROUTE]  api/v1/pesquisadores/
    # [ROUTE]  api/v1/pesquisadores/{id}/ 
    # [ROUTE]  api/v1/postagens/
    # [ROUTE]  api/v1/postagens/{id}/ 
    

    # NOTE
    #         Método    | URL                         | Ação            | Descrição
    # --------- | --------------------------- | --------------- | ---------------------------------------
    # GET       | /api/instituicoes/          | list            | Lista todas as instituições.
    # POST      | /api/instituicoes/          | create          | Cria uma nova instituição.
    # GET       | /api/instituicoes/{id}/     | retrieve        | Retorna os detalhes de uma instituição.
    # PUT       | /api/instituicoes/{id}/     | update          | Atualiza todos os campos de uma instituição.
    # PATCH     | /api/instituicoes/{id}/     | partial_update  | Atualiza alguns campos de uma instituição.
    # DELETE    | /api/instituicoes/{id}/     | destroy         | Deleta uma instituição.


    # [ROUTE]  api/v1/postagens/upload-image/
    path('api/v1/postagens-content/upload-image/', PostagemImagemUploadView.as_view(), name='postagem-imagem-upload'),

    #  . . . 🔓

    # [ROUTE]  api/v1/blog/posts/
    # [ROUTE]  api/v1/blog/posts/{id}/ 

    # [ROUTE]  api/v1/map-markers/
    path(
        'api/v1/map-markers/', 
        InstituicaoMarkerView.as_view(), 
        name='public-map-markers'
    ),


    # [ROUTE]  api/v1/profile/instituicoes/<int:pk>/
    path(
        'api/v1/profile/instituicoes/<int:pk>/', # A URL espera o ID da instituição
        PublicInstituicaoDetailView.as_view(), 
        name='public-instituicao-detail'
    ),



    # ── ⋙ ── ── ── Temp_cache_view ── ── ── ── ──➤

    # [ROUTE]  api/v1/cache_my_data/
    path("api/v1/cache_my_data/",Temp_cache_view.as_view(), name = "cash_data_view"),

    # ── ⋙ ── ── ── AgricultureData ── ── ── ── ──➤

    # [ROUTE] api/v1/getTopValues/
    path("api/v1/getTopValues/", TOPValuesView.as_view(), name="top_values_view"),

    # [ROUTE] api/v1/getTopSeries/
    path("api/v1/getTopSeries/", TopTimeSeriesView.as_view(), name="top_series_view"),

    # [ROUTE] api/v1/getRegionValues/
    path("api/v1/getRegionValues/", RegionValuesView.as_view(), name="top_series_view"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Incite Admin"
admin.site.site_title = "Incite Portal"
admin.site.index_title = "Incite Admin Portal"
