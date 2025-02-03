from dj_rest_auth.views import PasswordResetConfirmView
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from apps.users.views import DeleteUserView, DeleteAllUsersView, ListUsersView, GetUserRoleView
from apps.agricultura.views import TOPValuesView

from apps.cache.views import Temp_cache_view


schema_view = get_schema_view(
    openapi.Info(
        title="BI API Admin",
        default_version="v1",
        description="API documentation for HM API",
        contact=openapi.Contact(email="henry_melen@hotmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [

    path(settings.ADMIN_URL, admin.site.urls),
    
    # ┌─────────┐
    # │ Swagger │
    # └─────────┘

    path('api/v1/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("api/v1/redoc/", schema_view.with_ui("redoc", cache_timeout=0)),

    
    # ┌──────────────┐
    # │ df-rest-auth │
    # └──────────────┘

    path("api/v1/auth/", include("dj_rest_auth.urls")),
    path("api/v1/auth/registration/", include("dj_rest_auth.registration.urls")),
    path(
        "api/v1/auth/password/reset/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),



    # ── ⋙ ── ── ── Users ── ── ── ── ──➤

    # [ROUTE]  listUsersView
    path("api/v1/auth/listUsers/", ListUsersView.as_view(), name="user_details"),

    # [ROUTE]  DeleteUserView
    path("api/v1/auth/deleteUser/<int:pk>/", DeleteUserView.as_view(), name = "delete_user"),

    # [ROUTE]  DeleteAllUsersView
    path("api/v1/auth/deleteAll/", DeleteAllUsersView.as_view(), name = "delete_all_view"),

    # [ROUTE]  GetUserRoleView
    path("api/v1/auth/userRole/", GetUserRoleView.as_view(), name = "Get-roles-view"),



    # ── ⋙ ── ── ── Temp_cache_view ── ── ── ── ──➤

    # [ROUTE]  Temp_cache_view
    path("api/v1/cache_my_data/",Temp_cache_view.as_view(), name = "cash_data_view"),


    # ── ⋙ ── ── ── AgricultureData ── ── ── ── ──➤

    # [ROUTE] TOPValuesView
    path("api/v1/getTopValues/", TOPValuesView.as_view(), name="filter_view"),


]

admin.site.site_header = "crescer Admin"

admin.site.site_title = "crescer Portal"

admin.site.index_title = "crescer Admin Portal"
