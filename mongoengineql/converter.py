from __future__ import absolute_import

from mongoengine import fields

from graphene.core.types.scalars import ID, Boolean, Float, Int, String
from graphene.core.types.definitions import List

from mongoengineql.utils import import_single_dispatch
from .fields import ConnectionOrListField, MongoEngineDocumentField


singledispatch = import_single_dispatch()


@singledispatch
def convert_mongoengine_field(field):
    raise Exception(
        "Don't know how to convert the MongoEngine field %s (%s)" % (field, field.__class__))


@convert_mongoengine_field.register(fields.StringField)
@convert_mongoengine_field.register(fields.URLField)
@convert_mongoengine_field.register(fields.EmailField)
@convert_mongoengine_field.register(fields.DateTimeField)
@convert_mongoengine_field.register(fields.ComplexDateTimeField)
@convert_mongoengine_field.register(fields.BinaryField)
@convert_mongoengine_field.register(fields.FileField)
@convert_mongoengine_field.register(fields.ImageField)
@convert_mongoengine_field.register(fields.UUIDField)
def convert_field_to_string(field):
    return String()


@convert_mongoengine_field.register(fields.ObjectIdField)
def convert_field_to_id(field):
    return String()


@convert_mongoengine_field.register(fields.IntField)
@convert_mongoengine_field.register(fields.LongField)
def convert_field_to_int(field):
    return Int()


@convert_mongoengine_field.register(fields.BooleanField)
def convert_field_to_boolean(field):
    return Boolean()


@convert_mongoengine_field.register(fields.FloatField)
@convert_mongoengine_field.register(fields.DecimalField)
def convert_field_to_float(field):
    return Float()


@convert_mongoengine_field.register(fields.ListField)
@convert_mongoengine_field.register(fields.SortedListField)
def convert_field_to_graphql_list(field):
    return List(convert_mongoengine_field(field.field))


@convert_mongoengine_field.register(fields.EmbeddedDocumentListField)
def convert_field_to_graphql_list_field(field):
    return ConnectionOrListField(convert_mongoengine_field(field.field))


@convert_mongoengine_field.register(fields.EmbeddedDocumentField)
@convert_mongoengine_field.register(fields.ReferenceField)
def convert_field_to_graphql_field(field):
    document = field.document_type
    return MongoEngineDocumentField(document)
