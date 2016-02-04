from __future__ import absolute_import

from mongoengine import QuerySet
from mongoengine.document import EmbeddedDocument, Document

from graphene.utils import LazyList, ProxySnakeDict


def mongoengine_resolver(document, resolve_alias=None):
    def resolver(parent, args, info):
        if resolve_alias:
            m = ProxySnakeDict(resolve_alias)
            args = {m.get(k, k): v for k, v in args.items()}
        return document.objects.filter(**args)

    return resolver


def get_type_for_document(schema, document):
    types = schema.types.values()
    for _type in types:
        type_document = hasattr(_type, '_meta') and getattr(
            _type._meta, 'document', None)
        if document == type_document:
            return _type


def is_mapped(obj):
    return issubclass(obj, EmbeddedDocument) or issubclass(obj, Document)


class WrappedQueryset(LazyList):
    def __len__(self):
        # Dont calculate the length using len(queryset), as this will
        # evaluate the whole queryset and return it's length.
        # Use .count() instead
        return self._origin.count()


def maybe_queryset(value):
    if isinstance(value, QuerySet):
        return WrappedQueryset(value)
    return value


def import_single_dispatch():
    try:
        from functools import singledispatch
    except ImportError:
        singledispatch = None

    if not singledispatch:
        try:
            from singledispatch import singledispatch
        except ImportError:
            pass

    if not singledispatch:
        raise Exception(
            "It seems your python version does not include "
            "functools.singledispatch. Please install the 'singledispatch' "
            "package. More information here: "
            "https://pypi.python.org/pypi/singledispatch"
        )

    return singledispatch
