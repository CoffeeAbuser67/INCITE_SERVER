from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class ApiTestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cache'
    verbose_name = _("Cache App")