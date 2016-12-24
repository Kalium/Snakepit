import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import flask_restless_swagger
from flask_restless_swagger import SwagAPIManager as APIManager
from sqlalchemy.dialects.postgresql import JSON
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
default_db = "postgresql://pit:pit@localhost:5432/pit"
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('PIT_DB', default_db)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

flask_restless_swagger.sqlalchemy_swagger_type['JSON'] = "string"
manager = APIManager(app, flask_sqlalchemy_db=db)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.Unicode, unique=True)
    parent_hash = db.Column(db.Unicode, db.ForeignKey("item.hash"))
    parent = db.relationship("Item", backref="children", remote_side=[hash])
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(),
                           onupdate=db.func.now())


class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.Unicode)
    item_hash = db.Column(db.Unicode, db.ForeignKey("item.hash"))
    item = db.relationship("Item", backref=db.backref("data", lazy='dynamic'))
    data = db.Column(JSON)
    score = db.Column(db.Integer)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(),
                           onupdate=db.func.now())
    db.UniqueConstraint('key', 'item_hash')


class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matcher = db.Column(db.Unicode)

    # NB: Value can be negative...
    value = db.Column(db.Unicode)

    # This is the key that ties it to analysis data.
    analysis_key = db.Column(db.Unicode)

    # This is the key used to identify the rule uniquely.
    rule_key = db.Column(db.Unicode)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(),
                           onupdate=db.func.now())


manager.create_api(Item, primary_key='hash',
                   methods=['GET', 'POST', 'DELETE', 'PATCH'],
                   url_prefix='')
manager.create_api(Analysis, methods=['GET', 'POST', 'DELETE', 'PATCH'],
                   url_prefix='')
manager.create_api(Rule, primary_key="analysis_key",
                   methods=['GET', 'POST', 'DELETE', 'PATCH'],
                   url_prefix='')
db.create_all()

if __name__ == '__main__':
    app.run()
