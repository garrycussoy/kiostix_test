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
bp_penulis = Blueprint('penulis', __name__)
api = Api(bp_penulis)

'''
The following class is designed to get all writers and add new writer.
'''
class WriterResource(Resource):
    '''
    The following method is designed to prevent CORS.

    :param object self: A must present keyword argument
    :return: Status OK
    '''
    def options(self):
        return {'status': 'ok'}, 200
    
    '''
    The following method is designed to get all writers in database. Can also be searched by name

    :param object self: A must present keyword argument
    :return: Return all writers information which are stored in database
    '''
    def get(self):
        # Take input from user
        parser = reqparse.RequestParser()
        parser.add_argument('nama', location = 'args', required = False)
        args = parser.parse_args()

        # Query all writers
        writers = Penulis.query

        # Filter by name
        if args['nama'] != '' and args['nama'] != None:
            writers = writers.filter(Penulis.nama.like("%" + args['nama'] + "%"))
        
        # Show the result
        writers_list = []
        for writer in writers:
            writer = marshal(writer, Penulis.response_fields)
            writer_list.append(writer)
        return writers_list, 200

    '''
    The following method is designed to add new writer

    :param object self: A must present keyword argument
    :return: Return failure or success message, and return all information about the new writer if success
    '''
    def post(self):
        # Take input from users
        parser = reqparse.RequestParser()
        parser.add_argument('nama', location = 'json', required = True)
        parser.add_argument('nomor_hp', location = 'json', required = True)
        parser.add_argument('email', location = 'json', required = True)
        args = parser.parse_args()

        # Check emptyness
        if (args['nama'] == '' or args['nama'] is None)
        or (args['nomor_hp'] == '' or args['nomor_hp'] is None)
        or (args['email'] == '' or args['email'] is None):
            return {'pesan': 'Tidak boleh ada kolom yang dikosongkan'}, 400
        
        # ----- Check uniqueness -----
        # By phone number
        duplicate_phone = Penulis.query.filter_by(nomor_hp = args['nomor_hp']).first()
        if duplicate_phone is not None:
            return {'pesan': 'Nomor HP tersebut sudah digunakan oleh penulis lain'}, 409
        
        # By email
        duplicate_email = Penulis.query.filter_by(email = args['email']).first()
        if duplicate_email is not None:
            return {'pesan': 'Email tersebut sudah digunakan oleh penulis lain'}, 409
        
        # Create new record in database
        new_writer = Penulis(args['nama'], args['nomor_hp'], args['email'])
        db.session.add(new_writer)
        db.session.commit()

        # Return success message with the added writer information
        new_writer = marshal(new_writer, Penulis.response_fields)
        return {'pesan': 'Sukses menambahkan penulis', 'penulis_baru': new_writer}, 200

'''
The following class will provide CRUD functionality for writer specified by writer ID.
'''
class WriterResourceById(Resource):
    '''
    The following method is designed to prevent CORS.

    :param object self: A must present keyword argument
    :return: Status OK
    '''
    def options(self, writer_id):
        return {'status': 'ok'}, 200
    
    '''
    The following method is designed to get writer information from the given writer ID.

    :param object self: A must present keyword argument
    :param integer writer_id:
    :return: Return all information of specified writer
    '''
    def get(self, writer_id):
        # Search for related writer
        writer = Penulis.query.filter_by(id = writer_id).first()
        if writer is None:
            return {'pesan': 'Penulis yang kamu cari tidak ditemukan'}, 404
        writer = marshal(writer, Penulis.response_fields)
        return writer, 200
    
    '''
    The following method is designed to edit information of a writer

    :param object self: A must present keyword argument
    :param integer writer_id:
    :return: Return failure or success message, and return all information about the editted writer if success
    '''
    def put(self, writer_id):
        # Get the writer
        selected_writer = Penulis.query.filter_by(id = writer_id).first()
        if selected_writer is None:
            return {'pesan': 'Penulis yang ingin kamu ubah informasinya tidak ditemukan'}, 404

        # Take input from users
        parser = reqparse.RequestParser()
        parser.add_argument('nama', location = 'json', required = True)
        parser.add_argument('nomor_hp', location = 'json', required = True)
        parser.add_argument('email', location = 'json', required = True)
        args = parser.parse_args()

        # Check emptyness
        if (args['nama'] == '' or args['nama'] is None)
        or (args['nomor_hp'] == '' or args['nomor_hp'] is None)
        or (args['email'] == '' or args['email'] is None):
            return {'pesan': 'Tidak boleh ada kolom yang dikosongkan'}, 400
        
        # ----- Check uniqueness -----
        # By phone number
        duplicate_phone = Penulis.query.filter_by(nomor_hp = args['nomor_hp']).first()
        if duplicate_phone is not None:
            return {'pesan': 'Nomor HP tersebut sudah digunakan oleh penulis lain'}, 409
        
        # By email
        duplicate_email = Penulis.query.filter_by(email = args['email']).first()
        if duplicate_email is not None:
            return {'pesan': 'Email tersebut sudah digunakan oleh penulis lain'}, 409

        # Edit related record in database
        selected_writer.nama = args['nama']
        selected_writer.nomor_hp = args['nomor_hp']
        selected_writer.email = args['email']
        selected_writer.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.session.commit()

        # Return success message with the editted writer information
        selected_writer = marshal(selected_writer, Penulis.response_fields)
        return {'pesan': 'Sukses mengubah informasi penulis', 'penulis': selected_writer}, 200

# Endpoint in "penulis" route
api.add_resource(PenulisResource, '')
api.add_resource(PenulisResourceById, '/<writer_id>')