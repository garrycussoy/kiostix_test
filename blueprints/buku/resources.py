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
    
'''
The following class is designed to provide CRUD functionality of books based on the given book ID.
'''
class BookResourceById(Resource):
    '''
    The following method is designed to prevent CORS.

    :param object self: A must present keyword argument
    :param integer book_id:
    :return: Status OK
    '''
    def options(self, book_id):
        return {'status': 'ok'}, 200
    
    '''
    The following method is designed to get a book by ID.

    :param object self: A must present keyword argument
    :param integer book_id:
    :return: Return all information of specified book
    '''
    def get(self, book_id):
        # Query related book
        book = Buku.query.filter_by(id = book_id).first()
        if book is None:
            return {'pesan': 'Buku yang kamu cari tidak ditemukan'}, 404
        book = marshal(book, Buku.response_fields)

        # Search for the writer of  the book
        book_writers = PenulisBuku.query.filter_by(id_buku = book_id)
        writers = []
        for book_writer in book_writers:
            writer = Penulis.query.filter_by(id = id_penulis).first()
            writers.append(writer.nama)
        writers = ", ".join(writers)
        book['penulis'] = writers

        return available_books, 200
    
    '''
    The following method is designed to ediat a book.

    :param object self: A must present keyword argument
    :param integer book_id:
    :return: Return failure or success message, and return all information about the editted book if success
    '''
    def post(self, book_id):
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
        
        # ----- Edit record in database -----
        # Search for the book
        related_book = Buku.query.filter_by(id = book_id).first()
        if related_book is None:
            return {'pesan': 'Buku yang ingin kamu edit tidak ditemukan'}, 404

        # Check the existence of writer
        writers = []
        for writer_id in args['id_penulis']:
            # Check whether the id exists or not
            related_writer = Penulis.query.filter_by(id = writer_id).first()
            if related_writer is None:
                return {'pesan': 'Penulis dengan nomor ID ' + writer_id + ' tidak ada'}, 400
            writers.append(related_writer.nama)
        writers = ", ".join(writers)
        
        # Edit the record in "Buku" table
        related_book.id_kategori = args['id_kategori']
        related_book.judul = args['judul']
        related_book.penerbit = args['penerbit']
        related_book.nomor_isbn = args['nomor_isbn']
        related_book.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.session.commit()

        # Remove the old record in "PenulisBuku" table
        old_book_writers = PenulisBuku.query.filter_by(id_buku = book_id)
        for old_book_writer in old_book_writers:
            db.session.delete(old_book_writer)
            db.session.commit()
        
        # Add new record in "PenulisBuku" table
        for writer_id in args['id_penulis']:
            new_record = PenulisBuku(book_id, writer_id)
            db.session.add(new_record)
            db.session.commit()

        # Return the result
        related_book = marshal(related_book, Buku.response_fields)
        related_book['penulis'] = ", ".join(writers)
        return {'pesan': 'Sukses mengubah informasi buku', 'buku': related_book}, 200

# Endpoint in "buku" route
api.add_resource(BookResource, '')
api.add_resource(BookResourceById, '/<book_id>')