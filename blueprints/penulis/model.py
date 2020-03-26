# Import from standard libraries
from datetime import datetime, timedelta

# Import from related third party
from blueprints import db
from flask_restful import fields

'''
The following class is used to make the model of "Penulis" table.
'''
class Penulis(db.Model):
    # Define the property (each property associated with a column in database)
    __tablename__ = 'penulis'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nama = db.Column(db.String(255), nullable = False, default = '')
    nomor_hp = db.Column(db.String(255), nullable = False, default = '')
    email = db.Column(db.String(255), nullable = False, default = '')
    created_at = db.Column(db.DateTime, default = datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at = db.Column(db.DateTime, default = datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # The following dictionary is used to serialize "Penulis" instances into JSON form
    response_fields = {
        'id': fields.Integer,
        'nama': fields.String,
        'nomor_hp': fields.String,
        'email': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
    }

    # Required fields when create new instances of "Penulis" class
    def __init__(self, nama, nomor_hp, email):
        self.nama = nama
        self.nomor_hp = nomor_hp
        self.email = email

    # Reprsentative form to be shown in log
    def __repr__(self):
        return "Writer: " + self.nama