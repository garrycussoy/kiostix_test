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

            # Search the writers of the book
            writers = []
            book_writer_id = PenulisBuku.query.filter_by(id_buku = book['id'])
            for writer_id in book_writer_id:
                writer = Penulis.query.filter_by(id = writer_id.id_penulis).first()
                writer_name = writer.nama
                writers.append(writer_name)
            
            # Formatting the writers
            writers = ", ".join(writers)
            book["writer"] = writers

            available_books.append(book)
        return available_books, 200
    
    '''
    The following method is designed to post new book.

    :param object self: A must present keyword argument
    :return: Return failure or success message, and return all information about the inserted book if success
    '''
    def post(self):
        # Takke input from users
        parser = reqparse.RequestParser()
        parser.add_argument('id_kategori', location = 'json', required = True, type = int)
        parser.add_argument('judul', location = 'json', required = True)
        parser.add_argument('penerbit', location = 'json', required = True)
        parser.add_argument('nomor_isbn', location = 'json', required = True)
        parser.add_argument('id_penulis', location = 'json', required = True, type = list)
        args = parser.parse_args()

        # Check emptyness
        if (
            args['id_kategori'] == '' or args['id_kategori'] is None
            or args['judul'] == '' or args['judul'] is None
            or args['penerbit'] == '' or args['penerbit'] is None
            or args['nomor_isbn'] == '' or args['nomor_isbn'] is None
            or args['id_penulis'] == [] or args['id_penulis'] == '' or args['id_penulis'] is None
        ):
            return {'pesan': 'Tidak boleh ada kolom yang dikosongkan'}, 400
        
        # Check duplicate ISBN
        duplicate_isbn = Buku.query.filter_by(nomor_isbn = args['isbn']).first()
        if duplicate_isbn is not None:
            return {'pesan': 'Buku dengan nomor ISBN tersebut sudah ada di database'}, 409
        
        # ----- Create new record in database -----
        # Table "Buku"
        new_book = Buku(
            args['id_kategori'], args['judul'], args['penerbit'], args['nomor_isbn']
        )
        db.session.add(new_book)
        db.session.commit()
        new_book = marshal(new_book, Buku.response_fields)
        new_book['penulis'] = []

        # Table "PenulisBuku"
        for writer_id in args['id_penulis']:
            # Check whether the id exists or not
            related_writer = Penulis.query.filter_by(id = writer_id).first()
            if related_writer is None:
                return {'pesan': 'Penulis dengan nomor ID ' + writer_id + ' tidak ada'}, 400
            new_book['penulis'].append(related_writer.nama)

            # Create the record
            new_book_writer = PenulisBuku(new_book['id'], writer_id)
            db.session.add(new_book_writer)
            db.session.commit()
        
        # Return the result
        new_book['penulis'] = ", ".join(new_book['penulis'])
        return {'pesan': 'Sukses menambahkan buku', 'buku_baru': new_book}, 200

# Endpoint in "buku" route
api.add_resource(BookResource, '')