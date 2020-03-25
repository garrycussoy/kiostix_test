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
        formatted_category = []
        for category in available_categories:
            category = marshal(category, Kategori.response_fields)
            formatted_category.append(category)
        return formatted_category, 200
    
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
        available_categories = Kategori.query.filter_by(kategori = args['kategori'])
        if available_categories.first() is not None:
            return {'pesan': 'Kategori tersebut sudah ada'}, 409
        
        # Add new category to database
        new_category = Kategori(args['kategori'])
        db.session.add(new_category)
        db.session.commit()

        # Show the new category
        new_category = marshal(new_category, Kategori.response_fields)
        return {'pesan': 'Sukses menambahkan kategori', 'kategori_baru': new_category}, 200

'''
The following class is designed to provide CRUD functionality for categories by ID
'''
class CategoryResourceById(Resource):
    '''
    The following method is designed to prevent CORS.

    :param object self: A must present keyword argument
    :return: Status OK
    '''
    def options(self, category_id):
        return {'status': 'ok'}, 200
    
    '''
    The following method is designed to get specific category by ID

    :param object self: A must present keyword argument
    :param integer category_id:
    :return: Return specific category or a not-found message if the category doesn't exist
    '''
    def get(self, category_id):
        # Search for that specific category
        category = Kategori.query.filter_by(id = category_id).first()
        if category is None:
            return {'pesan': 'Kategori yang kamu cari tidak ditemukan'}, 404
        category = marshal(category, Kategori.response_fields)
        return category, 200
    
    '''
    The following method is designed to edit specific category by ID

    :param object self: A must present keyword argument
    :param integer category_id:
    :return: Return editted category or a failure message if the proccess failed 
    '''
    def put(self, category_id):
        # Search for that specific category
        category = Kategori.query.filter_by(id = category_id).first()
        if category is None:
            return {'pesan': 'Kategori yang ingin kamu ubah tidak ditemukan'}, 404
        
        # Take input from user
        parser = reqparse.RequestParser()
        parser.add_argument('kategori', location = 'json', required = True)
        args = parser.parse_args()

        # Check emptyness
        if args['kategori'] == None or args['kategori'] == '':
            return {'pesan': 'Kolom kategori tidak boleh dikosongkan'}, 400
        
        # Check uniqueness
        duplicate_category = Kategori.query.filter_by(kategori = args['kategori']).first()
        if duplicate_category is not None:
            return {'pesan': 'Kategori tersebut sudah ada'}, 409
        
        # Edit specific record in database
        category.kategori = args['kategori']
        category.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.session.commit()

        # Return the editted category
        category = marshal(category, Kategori.response_fields)
        return {'pesan': 'Sukses mengubah kategori', 'kategori': category}, 200
    
    '''
    The following method is designed to delete specific category by ID

    :param object self: A must present keyword argument
    :param integer category_id:
    :return: Return deleted category or a failure message if the proccess failed 
    '''
    def delete(self, category_id):
        # Search for that specific category
        category = Kategori.query.filter_by(id = category_id).first()
        if category is None:
            return {'pesan': 'Kategori yang ingin kamu hapus tidak ditemukan'}, 404
        
        # Check whether there is other record that references to this category
        books = Buku.query.filter_by(id_kategori = category_id).first()
        if books is not None:
            return {'pesan': 'Kamu tidak bisa menghapus kategori ini karena ada buku yang menggunakan kategori ini'}, 400

        # Delete specific record in database
        deleted_category = marshal(category, Kategori.response_fields)
        db.session.delete(category)
        db.session.commit()

        # Return the deleted category
        return {'pesan': 'Sukses menghapus kategori', 'kategori': deleted_category}, 200

# Endpoint in "kategori" route
api.add_resource(CategoryResource, '')
api.add_resource(CategoryResourceById, '/<category_id>')