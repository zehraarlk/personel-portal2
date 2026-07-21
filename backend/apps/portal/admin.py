from django.contrib import admin

from apps.portal.models import PORTAL_MODELS


SENSITIVE_EXCLUDE = {'sifre', 'remember_token_hash', 'remember_token_expires', 'tc_no'}


def _list_display(model):
    names = [f.name for f in model._meta.fields if f.name not in SENSITIVE_EXCLUDE]
    return tuple(names[:6]) or ('id',)


def _search_fields(model):
    fields = []
    for f in model._meta.fields:
        if f.name in SENSITIVE_EXCLUDE:
            continue
        if f.get_internal_type() in ('CharField', 'TextField'):
            fields.append(f.name)
    return fields[:5]


for model in PORTAL_MODELS:
    if model in admin.site._registry:
        continue

    opts = type(
        f'{model.__name__}Admin',
        (admin.ModelAdmin,),
        {
            'list_display': _list_display(model),
            'search_fields': _search_fields(model),
        },
    )
    admin.site.register(model, opts)
