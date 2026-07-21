from django.apps import AppConfig


class PortalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.portal'
    label = 'portal'
    verbose_name = 'Personel Portalı'

    def ready(self):
        # Django model adına otomatik İngilizce "s" eklemesin
        from apps.portal.models import PORTAL_MODELS

        for model in PORTAL_MODELS:
            label = model.__name__
            model._meta.verbose_name = label
            model._meta.verbose_name_plural = label
