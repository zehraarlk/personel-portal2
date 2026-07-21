from django.urls import include, path

from .router import PortalRouter
from .serializers import VIEWSETS, health

router = PortalRouter()
for model, viewset in VIEWSETS.items():
    router.register(model._meta.db_table, viewset, basename=model._meta.db_table)

urlpatterns = [
    path('health/', health, name='health'),
    path('', include(router.urls)),
]
