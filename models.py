# ----------------------------------------------------------------------------#
# Contains all Database configuration, models and relationships.
# ----------------------------------------------------------------------------#
import os
from sqlalchemy import Column, String, Integer, Date,ForeignKey
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.schema import  UniqueConstraint
import json

database_path = os.getenv('DATABASE_URL','')
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
binds a flask application and a SQLAlchemy service
'''
def setup_db(app,database_path=database_path):
    # based on proj1, load DB config from config.py
    # app.config.from_object('config')
    # print(f"database_path is: {database_path}")
    if database_path:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    db.app = app
    db.init_app(app)
    # print(f"app.config is: {app.config}")


# based on project 3 , reinit db
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    #moved init_db work to init_db.py


'''
Extend the base Model class to add common methods
'''
class BaseMethodClass(db.Model):
    __abstract__ = True

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
# Based on https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#association-object
# implement Movies and Actors models' many2many relationship with 'remuneration' Class
# defined composite columns' UniqueConstraints based on
# https://stackoverflow.com/questions/10059345/sqlalchemy-unique-across-multiple-columns
# to avoid duplicate items creation
class Remuneration(BaseMethodClass):
    __tablename__ = 'remuneration'
    id = db.Column(db.Integer,primary_key=True)
    movie_id = Column(Integer,ForeignKey('movies.id'), nullable=False)
    actor_id = Column(Integer,ForeignKey('actors.id'), nullable=False)
    remuneration= Column(Integer)
    actor=relationship("Actors",back_populates="movies")
    movie=relationship("Movies",back_populates="actors")
    __table_args__ = (UniqueConstraint('movie_id', 'actor_id', name='_movie_actor_uc'),)

    def format(self):
        return {
            'id': self.id,
            'movie_id': self.movie_id,
            'actor_id': self.actor_id,
            'remuneration': self.remuneration
        }


#Movies
class Movies(BaseMethodClass):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)
    # remuneration=db.relationship('Remuneration',backref='movies',lazy=True)
    actors=relationship('Remuneration',back_populates='movie')

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.strftime('%Y-%m-%d'),
            'actors': [actor.actor.name for actor in self.actors]
        }

    def __repr__(self):
        return f'<My Movie "{self.title}">'

class Actors(BaseMethodClass):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)
    age = Column(Integer)
    movies=relationship('Remuneration',back_populates='actor')
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age,
            'movies': [movie.movie.title for movie in self.movies]
        }
    def __repr__(self):
        return f'<My Actor "{self.name}">'
