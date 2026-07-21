from django.contrib import admin
from django.urls import include, path

from apps.portal.views import home

admin.site.site_header = 'Gebze Personel Portalı'
admin.site.site_title = 'Personel Portalı'
admin.site.index_title = 'Yönetim'

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('apps.portal.api.urls')),
]
