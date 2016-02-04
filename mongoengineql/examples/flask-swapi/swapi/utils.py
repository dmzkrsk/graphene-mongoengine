from __future__ import absolute_import

from .documents import *


def init_db():
    human = Character(
        name='Human',
        keywords=[Keyword(name='alive'), Keyword(name='has_hair')]
    )
    human.save()

    droid = Character(
        name='Droid',
        keywords=[Keyword(name='metallic'), Keyword(name='can_beep')]
    )
    droid.save()

    red = Color('red')
    red.save()
    blue = Color('blue')
    blue.save()
    green = Color('green')
    green.save()
    orange = Color('orange')
    orange.save()

    rebels = Faction(
        uid=1,
        name='Alliance to Restore the Republic',
        hero=human,
        keywords=['jedi', 'jungle', 'justice'],
        colors=[red]
    )
    rebels.save()

    empire = Faction(
        uid=2,
        name='Galactic Empire',
        hero=droid,
        keywords=['sith', 'march', 'wow'],
        colors=[blue, orange, green]
    )
    empire.save()

    xwing = Ship(
        name='X-Wing',
        faction=rebels,
        type=ShipType(name='starfighter')
    )
    xwing.save()

    ywing = Ship(
        uid=1,
        name='Y-Wing',
        faction=rebels,
        type=ShipType(name='starfighter')
    )
    ywing.save()

    awing = Ship(
        uid=2,
        name='A-Wing',
        faction=rebels,
        type=ShipType(name='starfighter')
    )
    awing.save()

    # Yeah, technically it's Corellian. But it flew in the service of the rebels,
    # so for the purposes of this demo it's a rebel ship.
    falcon = Ship(
        uid=3,
        name='Millenium Falcon',
        faction=rebels,
        type=ShipType(name='freighter')
    )
    falcon.save()

    homeOne = Ship(
        uid=4,
        name='Home One',
        faction=rebels,
        type=ShipType(name='cruiser')
    )
    homeOne.save()

    tieFighter = Ship(
        uid=5,
        name='TIE Fighter',
        faction=empire,
        type=ShipType(name='starfighter')
    )
    tieFighter.save()

    tieInterceptor = Ship(
        uid=6,
        name='TIE Interceptor',
        faction=empire,
        type=ShipType(name='starfighter')
    )
    tieInterceptor.save()

    executor = Ship(
        uid=7,
        name='Executor',
        faction=empire,
        type=ShipType(name='dreadnought')
    )
    executor.save()


def clear_db():
    Ship.drop_collection()
    Faction.drop_collection()
    Character.drop_collection()
