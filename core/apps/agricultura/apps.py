from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AgriculturaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.agricultura'
    verbose_name = _("Agricultura")


