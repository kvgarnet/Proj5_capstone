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
    #moved init_db to init_db.py
    # init_db()
# def init_db():
#     movie1 = Movies(title="You've got mails", release_date=date(1998,12,18))
#     movie2 = Movies(title='Forrest Gump', release_date=date(1994, 6, 23))
#     # movie3 = Movies(title='The Shawshank Redemption', release_date=date(1994, 9, 10))
#     db.session.add_all([movie1, movie2])
#     db.session.commit()
#
#     actor1 = Actors(name='Meg Ryan', gender='female', age=62)
#     actor2 = Actors(name='Tom Hanks', gender='male', age=66)
#     actor3 = Actors(name='Robin Wright', gender='female', age=56)
#     # actor4 = Actors(name='Morgan Freeman', gender='male', age=75)
#     # actor5 = Actors(name='Tim Robins', gender='male', age=64)
#
#     db.session.add_all([actor1, actor2, actor3])
#     db.session.commit()
#     # populate association table
#     movie1.actors.append(actor1)
#     movie1.actors.append(actor2)
#     movie2.actors=[actor2,actor3]
#
#     db.session.commit()
# Based on lesson 18,implement Movies and Actors models' many2many relationship with 'movie_actor_tb' Table
movie_actor_tb = db.Table('movie_actor_tb',
                   # db.Column('id', db.Integer, primary_key=True),
                   db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), nullable=False),
                   db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'), nullable=False)
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
    actors = db.relationship('Actors', secondary=movie_actor_tb, backref=db.backref('movies'), lazy=True)

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

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
