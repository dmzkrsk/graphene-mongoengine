from __future__ import absolute_import
import inspect

import six

from graphene.core.classtypes.objecttype import ObjectType, ObjectTypeMeta
from graphene.relay.types import Connection, Node, NodeMeta
from .converter import (convert_mongoengine_field)
from .options import MongoEngineOptions
from .utils import is_mapped


class MongoEngineObjectTypeMeta(ObjectTypeMeta):
    options_class = MongoEngineOptions

    def construct_fields(cls):
        only_fields = cls._meta.only_fields
        exclude_fields = cls._meta.exclude_fields
        already_created_fields = {f.attname for f in cls._meta.local_fields}

        all_fields = cls._meta.document._fields.values()

        for field in all_fields:
            is_not_in_only = only_fields and field.name not in only_fields
            is_already_created = field.name in already_created_fields
            is_excluded = field.name in exclude_fields or is_already_created
            if is_not_in_only or is_excluded:
                # We skip this field if we specify only_fields and is not
                # in there. Or when we excldue this field in exclude_fields
                continue
            converted_field = convert_mongoengine_field(field)
            cls.add_to_class(field.name, converted_field)

    def construct(cls, *args, **kwargs):
        cls = super(MongoEngineObjectTypeMeta, cls).construct(*args, **kwargs)
        if not cls._meta.abstract:
            if not cls._meta.document:
                raise Exception(
                    'MongoEngine ObjectType %s must have a document in the Meta class attr' %
                    cls)
            elif not inspect.isclass(cls._meta.document) or not is_mapped(cls._meta.document):
                raise Exception('Provided document in %s is not a MongoEngine document' % cls)

            cls.construct_fields()
        return cls


class InstanceObjectType(ObjectType):
    class Meta:
        abstract = True

    def __init__(self, _root=None):
        if _root:
            assert isinstance(_root, self._meta.document), (
                '{} received a non-compatible instance ({}) '
                'when expecting {}'.format(
                    self.__class__.__name__,
                    _root.__class__.__name__,
                    self._meta.document.__name__
                ))
        super(InstanceObjectType, self).__init__(_root=_root)

    @property
    def instance(self):
        return self._root

    @instance.setter
    def instance(self, value):
        self._root = value

    def __getattr__(self, attr):
        return getattr(self._root, attr)


class MongoEngineObjectType(
    six.with_metaclass(MongoEngineObjectTypeMeta, InstanceObjectType)):

    class Meta:
        abstract = True


class MongoEngineConnection(Connection):
    pass


class MongoEngineNodeMeta(MongoEngineObjectTypeMeta, NodeMeta):
    pass


class NodeInstance(Node, InstanceObjectType):

    class Meta:
        abstract = True


class MongoEngineNode(six.with_metaclass(
        MongoEngineNodeMeta, NodeInstance)):

    class Meta:
        abstract = True

    @classmethod
    def get_node(cls, id, info=None):
        try:
            instance = cls._meta.document.objects.get(id=id)
            return cls(instance)
        except cls._meta.document.DoesNotExist:
            return None