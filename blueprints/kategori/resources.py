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
bp_kategori = Blueprint('kategori', __name__)
api = Api(bp_kategori)

'''
The following class is designed to get all categories and add new category.
'''
class CategoryResource(Resource):
    '''
    The following method is designed to prevent CORS.

    :param object self: A must present keyword argument
    :return: Status OK
    '''
    def options(self):
        return {'status': 'ok'}, 200
    
    '''
    The following method is designed to get all available categories

    :param object self: A must present keyword argument
    :return: Return all available categories as an array
    '''
    def get(self):
        # Query all categories
        available_categories = Kategori.query

        # Format the array and return is as a result
        for category in available_categories:
            category = marshal(category, Kategori.response_fields)
        return available_categories, 200
    
    '''
    The following method is designed to add new category

    :param object self: A must present keyword argument
    :return: Return all information about that new category
    '''
    def post(self):
        # Take input from user
        parser = reqparse.RequestParser()
        parser.add_argument('kategori', location = 'json', required = True)
        args = parser.parse_args()

        # Check emptyness
        if args['kategori'] == None or args['kategori'] == '':
            return {'pesan': 'Kolom kategori tidak boleh dikosongkan'}, 400
        
        # Validate whether the category has already exist or not
        available_categories = Kategori.query
        if available_categories.first() is not None:
            return {'pesan': 'Kategori tersebut sudah ada'}, 409
        
        # Add new category to database
        new_category = Kategori(args['kategori'])
        db.session.add(new_category)
        db.session.commit()

        # Show the new category
        return {'pesan': 'Sukses menambahkan kategori', 'kategori_baru': new_category}, 200

# Endpoint in problem-collection route
api.add_resource(CategoryResource, '')

'''
The following class is designed to get all categories and add new category.
'''
class CategoryResource(Resource):
    '''
    The following method is designed to prevent CORS.

    :param object self: A must present keyword argument
    :return: Status OK
    '''
    def options(self):
        return {'status': 'ok'}, 200
    
    '''
    The following method is designed to get all available categories

    :param object self: A must present keyword argument
    :return: Return all available categories as an array
    '''
    def get(self):