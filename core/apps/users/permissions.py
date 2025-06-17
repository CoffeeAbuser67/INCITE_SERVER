# users/permissions.py
from rest_framework.permissions import BasePermission

class IsAdminOrIsSelf(BasePermission):
    """
    NOTE
    Permite acesso total para admins (is_staff).
    Permite que usuários não-admin vejam e editem seus próprios perfis, mas não o de outros.
    """
    def has_object_permission(self, request, view, obj):
        # Admins podem fazer tudo com qualquer objeto
        if request.user.is_staff:
            return True
        # O usuário logado é o mesmo objeto que está tentando acessar?
        return obj == request.user