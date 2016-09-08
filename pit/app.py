import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import flask_restless_swagger
from flask_restless_swagger import SwagAPIManager as APIManager
from sqlalchemy.dialects.postgresql import JSON
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/swagger.json": {"origins": "*"}})
default_db = "postgresql://pit:pit@localhost:5432/pit"
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('PIT_DB', default_db)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

flask_restless_swagger.sqlalchemy_swagger_type['JSON'] = "string"
manager = APIManager(app, flask_sqlalchemy_db=db)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String(64))
    parent_id = db.Column(db.Integer, db.ForeignKey("item.id"))
    parent = db.relationship("Item", backref="children", remote_side=[id])
    data = db.relationship("Analysis")


class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"))
    item = db.relationship("Item")
    data = db.Column(JSON)

manager.create_api(Item, methods=['GET', 'POST', 'DELETE', 'PATCH'])
manager.create_api(Analysis, methods=['GET', 'POST', 'DELETE', 'PATCH'])

if __name__ == '__main__':
    db.create_all()
    app.run()
