# Import from standard libraries
import json
import os
from datetime import timedelta
from functools import wraps

# Import from related third party
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS

# A step to prevent CORS
app = Flask(__name__)
CORS(app)

# Set the following to true, if you want to auto-reload when there is a change, or false otherwise
app.config['APP_DEBUG'] = True

# ---------- Database Setup ----------
# Connect to database
try:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Garryac1@localhost:3306/kiostix_test'
except Exception as e:
    raise e

# Setup database migration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
# ---------- End of database setup ----------

# Import modules related to routing
from blueprints.buku.resources import bp_buku
from blueprints.kategori.resources import bp_kategori
from blueprints.penulis.resources import bp_penulis

# Register routes
app.register_blueprint(bp_kategori, url_prefix='/kategori')
app.register_blueprint(bp_buku, url_prefix='/buku')
app.register_blueprint(bp_penulis, url_prefix='/penulis')

# Create the database
db.create_all()

# Handle response from a request
@app.after_request
def after_request(response):
    try:
        request_data = response.get_json()
    except Exception as e:
        request_data = response.args.to_dict()
    
    log_data = json.dumps({
        'status_code': response.status_code,
        'method': request.method,
        'code': response.status,
        'uri': request.full_path,
        'requedatetimest': request_data,
        'response': json.loads(response.data.decode('utf-8'))
    })
    log = app.logger.info("REQUEST_LOG\t%s", log_data) if response.status_code == 200 else app.logger.warning("REQUEST_LOG\t%s", log_data)
    return response