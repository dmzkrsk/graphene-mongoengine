from __future__ import unicode_literals
from __future__ import absolute_import

from mongoengine import *


class Keyword(EmbeddedDocument):
    name = StringField(max_length=50)


class Character(Document):
    name = StringField(max_length=50)
    keywords = EmbeddedDocumentListField(Keyword)

    def __str__(self):
        return self.name


class Color(Document):
    name = StringField(max_length=20)

    def __str__(self):
        return self.name


class Faction(Document):
    uid = IntField(unique=True)
    name = StringField(max_length=50)
    hero = ReferenceField(Character)
    keywords = ListField(StringField())
    colors = ListField(ReferenceField(Color))

    def __str__(self):
        return self.name


class ShipType(EmbeddedDocument):
    name = StringField()

    def __str__(self):
        return self.name


class Ship(Document):
    uid = IntField(unique=True)
    name = StringField(max_length=50)
    type = EmbeddedDocumentField(ShipType)
    faction = ReferenceField(Faction)

    def __str__(self):
        return self.name


def get_ships():
    return Ship.objects.all()


def get_faction(_id):
    return Faction.objects.get(id=_id)


def get_ship(_id):
    return Ship.objects.get(id=_id)


def get_rebels():
    return Faction.objects.get(uid=1)


def get_empire():
    return Faction.objects.get(uid=2)