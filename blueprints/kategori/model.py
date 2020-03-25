# Import from standard libraries
from datetime import datetime, timedelta

# Import from related third party
from blueprints import db
from flask_restful import fields

'''
The following class is used to make the model of "Kategori" table.
'''
class Kategori(db.Model):
    # Define the property (each property associated with a column in database)
    __tablename__ = 'kategori'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    kategori = db.Column(db.String(255), nullable = False, default = '')
    created_at = db.Column(db.DateTime, default = datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at = db.Column(db.DateTime, default = datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # The following dictionary is used to serialize "Kategori" instances into JSON form
    response_fields = {
        'id': fields.Integer,
        'kategori': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
    }

    # Required fields when create new instances of "Kategori" class
    def __init__(self, kategori):
        self.kategori = kategori

    # Reprsentative form to be shown in log
    def __repr__(self):
        return "Category: " + self.kategori