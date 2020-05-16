import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

database_name = os.getenv('DB_NAME',"capstone")
user = os.getenv('DB_USER','postgres')
password = os.getenv('DB_PASSWORD', '123456789')
ip_server = os.getenv('DB_IP_SERVER', 'localhost')
port = os.getenv('DB_PORT','5432')
database_path = f"postgres+psycopg2://{user}:{password}@{ip_server}:{port}/{database_name}"

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL', database_path)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    #db.drop_all()
    db.create_all()
    return db

class Movie(db.Model):
    __tablename__ = 'Movies'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    release_date = db.Column(db.String)
    actors = db.relationship('Actor', backref = 'movie', lazy = True)
    def format(self):
        return {
                'id': self.id,
                'title': self.title,
                'release_date': self.release_date
                }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def rollback(self):
        db.session.rollback()
    
    def __repre__(self):
        return json.dumps(self.format())

class Actor(db.Model):
    __tablename__ = 'Actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    gender = db.Column(db.String)
    age = db.Column(db.Integer)
    movie_id = db.Column(db.Integer, db.ForeignKey('Movies.id'), nullable= False)

    def format(self):
        return {
                'id': self.id,
                'name': self.name,
                'gender': self.gender,
                'age': self.age
        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def rollback():
        db.session.rollback()
    
    def __repre__(self):
        return json.dumps(self.format())
