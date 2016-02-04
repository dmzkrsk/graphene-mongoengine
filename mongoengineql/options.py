from __future__ import absolute_import
from graphene.core.classtypes.objecttype import ObjectTypeOptions
from graphene.relay.types import Node
from graphene.relay.utils import is_node

VALID_ATTRS = ('document', 'only_fields', 'exclude_fields')


class MongoEngineOptions(ObjectTypeOptions):
    def __init__(self, *args, **kwargs):
        super(MongoEngineOptions, self).__init__(*args, **kwargs)
        self.document = None
        self.valid_attrs += VALID_ATTRS
        self.only_fields = None
        self.exclude_fields = []
        self.filter_fields = None
        self.filter_order_by = None

    def contribute_to_class(self, cls, name):
        super(MongoEngineOptions, self).contribute_to_class(cls, name)
        if is_node(cls):
            self.exclude_fields = list(self.exclude_fields) + ['id']
            self.interfaces.append(Node)
