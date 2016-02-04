from __future__ import absolute_import
from graphene.core.exceptions import SkipField
from graphene.core.fields import Field
from graphene.core.types.base import FieldType
from graphene.core.types.definitions import List
from graphene.relay import ConnectionField
from graphene.relay.utils import is_node
from .utils import get_type_for_document, maybe_queryset, mongoengine_resolver


class MongoEngineConnectionField(ConnectionField):
    @property
    def document(self):
        return self.type._meta.document

    def from_list(self, connection_type, resolved, args, info):
        if not resolved:
            resolved = mongoengine_resolver(self.document)(self, args, info)
        resolved_qs = maybe_queryset(resolved)
        return super(MongoEngineConnectionField, self).from_list(connection_type, resolved_qs, args, info)


class ConnectionOrListField(Field):
    def internal_type(self, schema):
        document_field = self.type
        field_object_type = document_field.get_object_type(schema)
        if not field_object_type:
            raise SkipField()
        if is_node(field_object_type):
            field = MongoEngineConnectionField(field_object_type)
        else:
            field = Field(List(field_object_type))
        field.contribute_to_class(self.object_type, self.attname)
        return schema.T(field)


class MongoEngineDocumentField(FieldType):
    def __init__(self, document, *args, **kwargs):
        self.document = document
        super(MongoEngineDocumentField, self).__init__(*args, **kwargs)

    def internal_type(self, schema):
        _type = self.get_object_type(schema)
        if not _type and self.parent._meta.only_fields:
            raise Exception(
                    "Collection %r is not accessible by the schema. "
                    "You can either register the type manually "
                    "using @schema.register. "
                    "Or disable the field in %s" % (
                        self.document,
                        self.parent,
                    )
            )
        if not _type:
            raise SkipField()
        return schema.T(_type)

    def get_object_type(self, schema):
        return get_type_for_document(schema, self.document)

    def List(self):
        return List(self, *self.args, **self.kwargs)
