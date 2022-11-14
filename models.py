# ----------------------------------------------------------------------------#
# Contains all Database configuration, models and relationships.
# ----------------------------------------------------------------------------#
import os
from sqlalchemy import Column, String, Integer, Date
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import json

# database_path = os.environ['DATABASE_URL']
# if database_path.startswith("postgres://"):
#   database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app):
    # based on proj1, load DB config from config.py
    app.config.from_object('config')
    db.app = app
    db.init_app(app)


# based on project 3 , reinit db
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    #moved init_db work to init_db.py

# Based on lesson 18,implement Movies and Actors models' many2many relationship with 'actor_remuneration' Table
actor_remuneration = db.Table('actor_remuneration',
                   # db.Column('id', db.Integer, primary_key=True),
                   db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), nullable=False),
                   db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'), nullable=False),
                   db.Column('remuneration', db.Integer)
                              )


'''
Movie
Have title and release year
'''


class Movies(db.Model):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)
    actors = db.relationship('Actors', secondary=actor_remuneration, backref=db.backref('movies'), lazy=True)

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

    def close(self):
        db.session.close()

    def __repr__(self):
        return f'<My Movie "{self.title}">'

class Actors(db.Model):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)
    age = Column(Integer)

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age
        }
    def __repr__(self):
        return f'<My Actor "{self.name}">'

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

    def close(self):
        db.session.close()