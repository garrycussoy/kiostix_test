# Import from standard libraries
from datetime import datetime, timedelta

# Import from related third party
from blueprints import db
from flask_restful import fields

# Import other models
from blueprints.buku.model import Buku
from blueprints.penulis.model import Penulis

'''
The following class is used to make the model of "PenulisBuku" table.
'''
class PenulisBuku(db.Model):
    # Define the property (each property associated with a column in database)
    __tablename__ = 'penulis_buku'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_buku = db.Column(db.Integer, db.ForeignKey('buku.id'), nullable = False)
    id_penulis = db.Column(db.Integer, db.ForeignKey('penulis.id'), nullable = False)

    # The following dictionary is used to serialize "PenulisBuku" instances into JSON form
    response_fields = {
        'id': fields.Integer,
        'id_buku': fields.Integer,
        'id_penulis': fields.Integer
    }

    # Required fields when create new instances of "PenulisBuku" class
    def __init__(self, id_buku, id_penulis):
        self.id_buku = id_buku
        self.id_penulis = id_penulis

    # Reprsentative form to be shown in log
    def __repr__(self):
        return "Book ID " + str(self.id_buku) + " (Writer ID : " + str(self.id_penulis) + ")"