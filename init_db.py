from models import db_drop_and_create_all, db,Movies,Actors,movie_actor_tb
from datetime import date
from app import create_app
create_app()
db_drop_and_create_all()
movie1 = Movies(title="You've got mails", release_date=date(1998,12,18))
movie2 = Movies(title='Forrest Gump', release_date=date(1994, 6, 23))
# movie3 = Movies(title='The Shawshank Redemption', release_date=date(1994, 9, 10))
db.session.add_all([movie1, movie2])
db.session.commit()

actor1 = Actors(name='Meg Ryan', gender='female', age=62)
actor2 = Actors(name='Tom Hanks', gender='male', age=66)
actor3 = Actors(name='Robin Wright', gender='female', age=56)
# actor4 = Actors(name='Morgan Freeman', gender='male', age=75)
# actor5 = Actors(name='Tim Robins', gender='male', age=64)

db.session.add_all([actor1, actor2, actor3])
db.session.commit()
# populate association table
movie1.actors.append(actor1)
movie1.actors.append(actor2)
movie2.actors=[actor2,actor3]

db.session.commit()