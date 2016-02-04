from __future__ import absolute_import

import graphene
from graphene import relay
import mongoengineql
from . import documents

schema = graphene.Schema(name='Starwars Relay Schema')


@schema.register
class Keyword(mongoengineql.MongoEngineObjectType):

    class Meta:
        document = documents.Keyword


class Ship(mongoengineql.MongoEngineNode):

    class Meta:
        document = documents.Ship

    @classmethod
    def get_node(cls, id, info):
        return Faction(documents.get_ship(id))


@schema.register
class Character(mongoengineql.MongoEngineObjectType):

    class Meta:
        document = documents.Character


@schema.register
class Color(mongoengineql.MongoEngineObjectType):

    class Meta:
        document = documents.Color


class Faction(mongoengineql.MongoEngineNode):

    class Meta:
        document = documents.Faction

    @classmethod
    def get_node(cls, id, info):
        return Faction(documents.get_faction(id))


class Query(graphene.ObjectType):
    node = relay.NodeField()

    rebels = graphene.Field(Faction)
    empire = graphene.Field(Faction)

    all_ships = relay.ConnectionField(Ship, description='All the ships.')

    def resolve_all_ships(self, args, info):
        return documents.get_ships()

    def resolve_rebels(self, args, info):
        return documents.get_rebels()

    def resolve_empire(self, args, info):
        return documents.get_empire()

    # Non Relay example
    ships = mongoengineql.MongoEngineDocumentField(documents.Ship,
                           name=graphene.String(),
                           of=graphene.String(),
                       ).List()

    resolve_ships = mongoengineql.mongoengine_resolver(documents.Ship, {
        'of': 'type__name'  # search alias
    })


schema.query = Query
