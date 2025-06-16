
#  User
import uuid
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

#  User Manager 
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from allauth.account.models import EmailAddress

import logging
logger = logging.getLogger(__name__)
# ── ⋙── ── ── ── ── ── ── ──➤


# (✪) UserManager
class UserManager(BaseUserManager):

    # (●) email_validator
    def email_validator(self, email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            raise ValueError(_("You must provide a valid email address."))
        

    # (●) create_user
    def create_user(self, first_name, last_name, email, password, user_group=11, **extra_fields):
        """
        Cria um usuário normal. Se user_group não for fornecido, ele será um usuário comum (3).
        """

        logger.info("● create_user foi chamado")  # Log de debug

        if not first_name:
            raise ValueError(_("Users must have a first name."))
        if not last_name:
            raise ValueError(_("Users must have a last name."))
        if not email:
            raise ValueError(_("Users must have an email address."))

        email = self.normalize_email(email)
        self.email_validator(email)

        # Define permissões baseado no grupo

        if user_group not in [67, 22, 11]:
            user_group = 11

        is_staff, is_superuser = {
            67: (True, True),  
            22: (True, False), 
            11: (False, False)
        }.get(user_group, (False, False))  

        
        extra_fields.setdefault("is_staff", is_staff)
        extra_fields.setdefault("is_superuser", is_superuser)

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            user_group=user_group,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)

        EmailAddress.objects.get_or_create(user=user, email=email, defaults={"verified": True, "primary": True})

        return user

    # (●) create_superuser
    def create_superuser(self, first_name, last_name, email, password, **extra_fields):

        if not password:
            raise ValueError(_("Superuser must have a password."))

        return self.create_user(first_name, last_name, email, password, user_group=67, **extra_fields)
# ── ⋙── ── ── ── ── ── ── ──➤



# ★ User 
class User(AbstractBaseUser):

    logger.info("User Model being invoked. ")  # [LOG] ★ User

    # {●} UserGroup
    class UserGroup(models.IntegerChoices):
        ADMIN = 67, _("Master")
        MEMBRO = 11, _("Usuário Básico")


    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(verbose_name=_("first name"), max_length=50, default='')     
    last_name = models.CharField(verbose_name=_("last name"), max_length=50, default='')
    email = models.EmailField(
        verbose_name=_("email address"), db_index=True, unique=True
    )

    user_group = models.IntegerField(choices=UserGroup.choices, default=UserGroup.MEMBRO)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    # (○) UserManager
    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.first_name

    @property
    def get_full_name(self):
        return f"{self.first_name.title()} {self.last_name.title()}"

    @property
    def get_short_name(self):
        return self.first_name


    # (●) has_permission
    def has_permission(self, permission_name):
        permissions = {
            67: ["manage_posts", "manage_users"],
            11: []
        }
        return permission_name in permissions.get(self.user_group, [])
# ── ⋙── ── ── ── ── ── ── ──➤