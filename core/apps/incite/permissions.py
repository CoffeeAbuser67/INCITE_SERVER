from rest_framework.permissions import BasePermission


class IsPostAuthorOrAdmin(BasePermission):
    """
    Permite acesso total para admins.
    Permite que usuários básicos editem/deletem apenas posts que eles criaram
    ou que pertençam a uma instituição que eles criaram.
    """

    def has_object_permission(self, request, view, obj):
        # Admins (staff) podem fazer tudo
        if request.user.is_staff:
            return True

        # Se for um post geral (sem instituição), apenas o autor pode mexer
        if obj.instituicao is None:
            return obj.autor == request.user

        # Se for um post de instituição, o criador da instituição ou o autor do post podem mexer
        return obj.instituicao.criador == request.user or obj.autor == request.user
