from collections import OrderedDict

from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.routers import APIRootView, DefaultRouter


class PortalAPIRootView(APIRootView):
    """Personel Portalı API — personel_db uç noktaları"""

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        data = OrderedDict()
        data['health'] = reverse('health', request=request)
        data.update(response.data)
        return Response(data)


class PortalRouter(DefaultRouter):
    APIRootView = PortalAPIRootView
