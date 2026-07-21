from rest_framework import serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection

from apps.portal.models import PORTAL_MODELS, Duyuru, Personel


SENSITIVE_FIELDS = {'sifre', 'remember_token_hash', 'remember_token_expires', 'tc_no'}


def make_serializer(model):
    field_names = [
        f.name
        for f in model._meta.fields
        if f.name not in SENSITIVE_FIELDS
    ]

    meta = type(
        'Meta',
        (),
        {
            'model': model,
            'fields': field_names,
        },
    )

    attrs = {'Meta': meta}

    # Duyuru API uyumluluğu (React)
    if model.__name__ == 'Duyurular':
        attrs['ozet'] = serializers.SerializerMethodField()
        attrs['icerik'] = serializers.CharField(source='aciklama', read_only=True)
        meta.fields = list(field_names) + ['ozet', 'icerik']

        def get_ozet(self, obj):
            text = (obj.aciklama or '').strip()
            if len(text) <= 140:
                return text
            return text[:140].rstrip() + '…'

        attrs['get_ozet'] = get_ozet

    return type(f'{model.__name__}Serializer', (serializers.ModelSerializer,), attrs)


def make_viewset(model, serializer_class):
    return type(
        f'{model.__name__}ViewSet',
        (viewsets.ReadOnlyModelViewSet,),
        {
            'queryset': model.objects.all(),
            'serializer_class': serializer_class,
        },
    )


SERIALIZERS = {m: make_serializer(m) for m in PORTAL_MODELS}
VIEWSETS = {m: make_viewset(m, SERIALIZERS[m]) for m in PORTAL_MODELS}

# Geriye uyumlu isimler
DuyuruSerializer = SERIALIZERS[Duyuru]
PersonelSerializer = SERIALIZERS[Personel]
DuyuruViewSet = VIEWSETS[Duyuru]
PersonelViewSet = VIEWSETS[Personel]


@api_view(['GET'])
def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT DATABASE()')
            row = cursor.fetchone()
            db_name = row[0] if row else None
    except Exception as exc:  # noqa: BLE001
        return Response(
            {
                'status': 'error',
                'message': f'Veritabanı bağlantısı başarısız: {exc}',
                'database': None,
            },
            status=503,
        )

    counts = {}
    for model in PORTAL_MODELS:
        try:
            counts[model._meta.db_table] = model.objects.count()
        except Exception:  # noqa: BLE001
            counts[model._meta.db_table] = None

    return Response({
        'status': 'ok',
        'message': 'Gebze Personel Portalı API çalışıyor',
        'database': db_name,
        'tables': counts,
        'duyuru_count': counts.get('duyurular'),
        'personel_count': counts.get('personeller'),
    })
