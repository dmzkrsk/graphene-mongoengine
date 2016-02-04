from flask import Flask
from swapi.utils import init_db, clear_db
from mongoengine import connect

from swapi.schema import schema
from flask_graphql import GraphQL

app = Flask(__name__)
app.debug = True

GraphQL(app, schema=schema)


if __name__ == '__main__':
    connect('swapi')
    clear_db()
    init_db()
    app.run()
