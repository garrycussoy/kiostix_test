# Import from standard libraries
import json
import math
from datetime import datetime, timedelta, date

# Import from related third party
from blueprints import db, app
from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc

# Import models
from blueprints.buku.model import Buku
from blueprints.penulis.model import Penulis
from blueprints.kategori.model import Kategori
from blueprints.penulis_buku.model import PenulisBuku

# Creating blueprint
bp_buku = Blueprint('buku', __name__)
api = Api(bp_buku)

'''
The following class is designed to create new book and get all available books.
'''
class BookResource(Resource):
    '''
    The following method is designed to prevent CORS.

    :param object self: A must present keyword argument
    :return: Status OK
    '''
    def options(self):
        return {'status': 'ok'}, 200
    
    '''
    The following method is designed to get all available books.

    :param object self: A must present keyword argument
    :return: Return all available books
    '''
    def get(self):
        # Query all available books
        books = Buku.query

        # Formatting the result and show it
        available_books = []
        for book in books:
            book = marshal(book, Buku.response_fields)
            available_books.append(book)
        return available_books, 200

# Endpoint in "buku" route
api.add_resource(BookResource, '')