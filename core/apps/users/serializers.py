from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model

from rest_framework import serializers
import logging

from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)
User = get_user_model()
# ── ⋙ ── ── ── ── ── ── ── ──➤



# {✪} UserSerializer - Output Serializer 
class UserSerializer(serializers.ModelSerializer): 

    class Meta:
        model = User
        fields = [
            "pkid",
            "email",
            "first_name",
            "last_name",
            "user_group",
        ]


# {✪} CustomRegisterSerializer - Input Serializer
class CustomRegisterSerializer(RegisterSerializer):
    username = None
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    user_group = serializers.IntegerField(required=False)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)


    def get_cleaned_data(self):
        super().get_cleaned_data()
        return {
            "email": self.validated_data.get("email", ""),
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
            "password1": self.validated_data.get("password1", ""),
            "user_group": self.validated_data.get("user_group", User.UserGroup.CLIENTE),  # Padrão: usuário comum
        }

    def save(self, request):
        logger.info("● save() called ")
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()

        user.email = self.cleaned_data.get("email")
        user.set_password(self.cleaned_data.get("password1"))
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")

        # Se o miseravi mandar uma opcao nao valida.
        user_group = self.cleaned_data.get("user_group")
        if user_group not in [67, 22, 11]:
            user_group = 11
        user.user_group = user_group

        is_staff, is_superuser = {
            67: (True, True),  
            22: (True, False), 
            11: (False, False)
        }.get(user_group, (False, False))  

        user.is_staff = is_staff
        user.is_superuser = is_superuser

        user = adapter.save_user(request, user, self)
        user.save()
        setup_user_email(request, user, [])
        return user
# ── ⋙ ── ── ── ── ── ── ── ──➤







