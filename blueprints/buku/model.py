# Import from standard libraries
from datetime import datetime, timedelta

# Import from related third party
from blueprints import db
from flask_restful import fields

# Import other models
from blueprints.kategori.model import Kategori

'''
The following class is used to make the model of "Buku" table.
'''
class Buku(db.Model):
    # Define the property (each property associated with a column in database)
    __tablename__ = 'buku'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_kategori = db.Column(db.Integer, db.ForeignKey('kategori.id'), nullable = False)
    judul = db.Column(db.String(255), nullable = False, default = '')
    penerbit = db.Column(db.String(255), nullable = False, default = '')
    nomor_isbn = db.Column(db.String(255), nullable = False, default = '')
    created_at = db.Column(db.DateTime, default = datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at = db.Column(db.DateTime, default = datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # The following dictionary is used to serialize "Buku" instances into JSON form
    response_fields = {
        'id': fields.Integer,
        'id_kategori': fields.Integer,
        'judul': fields.String,
        'penerbit': fields.String,
        'nomor_isbn': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
    }

    # Required fields when create new instances of "Buku" class
    def __init__(
        self, id_kategori, judul, penerbit, nomor_isbn
    ):
        self.id_kategori = id_kategori
        self.judul = judul
        self.penerbit = penerbit
        self.nomor_isbn = nomor_isbn

    # Reprsentative form to be shown in log
    def __repr__(self):
        return "Title: " + self.judul