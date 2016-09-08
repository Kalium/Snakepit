import os
from flask import Flask
# from flask_restplus import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy.dialects.postgresql import JSON

app = Flask(__name__)
default_db = "postgresql://pit:pit@localhost:5432/pit"
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('PIT_DB', default_db)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String(64))
    parent_id = db.Column(db.Integer, db.ForeignKey("item.id"))
    parent = db.relationship("parent")
    children = db.relationship("Item", back_populates="parent")
    data = db.relationship("Analysis", back_populates="item")


class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"))
    item = db.relationship("item")
    data = db.Column(JSON)

if __name__ == '__main__':
    manager.run()
