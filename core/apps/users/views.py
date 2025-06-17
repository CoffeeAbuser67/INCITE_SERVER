
# users/views.py
from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from .serializers import UserSerializer # O serializer que você já tem
from .permissions import IsAdminOrIsSelf # Nossa nova permissão

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    NOTE
    API endpoint para ver, criar, editar e deletar usuários.
    - Admins veem todos os usuários.
    - Usuários comuns não conseguem listar todos os usuários.
    - Um usuário só pode ver/editar/deletar seu próprio perfil (a menos que seja admin).
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrIsSelf]

    def get_queryset(self):
        # Admins veem todos, usuários comuns só veem a si mesmos.
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(pk=user.pk)