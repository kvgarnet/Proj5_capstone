import argparse,os
from models import setup_db,db_drop_and_create_all, db,Movies,Actors,Remuneration
from datetime import date
from app import create_app
from config import db_path,test_db_path

def init_db(database_path):
    #import create_app is enough for DB init,below to be commented out
    app=create_app()
    setup_db(app,database_path)
    #drop and init only run for init
    db_drop_and_create_all()
    movie1 = Movies(title="You've got mails", release_date=date(1998,12,18))
    movie2 = Movies(title='Forrest Gump', release_date=date(1994, 6, 23))
    movie3 = Movies(title='The Shawshank Redemption', release_date=date(1994, 9, 10))
    db.session.add_all([movie1, movie2,movie3])
    db.session.commit()

    actor1 = Actors(name='Meg Ryan', gender='female', age=62)
    actor2 = Actors(name='Tom Hanks', gender='male', age=66)
    actor3 = Actors(name='Robin Wright', gender='female', age=56)
    # actor4 = Actors(name='Morgan Freeman', gender='male', age=75)
    # actor5 = Actors(name='Tim Robins', gender='male', age=64)


    db.session.add_all([actor1, actor2, actor3])
    db.session.commit()
    # populate association table
    # movie1.actors.append(actor1)
    # movie1.actors.append(actor2)
    # movie2.actors=[actor2,actor3]
    # db.session.commit()

    remuneration1 = Remuneration(
        movie_id = movie1.id,
        actor_id = actor1.id,
        remuneration = 500.00
    )
    remuneration2 = Remuneration(
        movie_id = movie1.id,
        actor_id = actor2.id,
        remuneration = 600.00
    )
    remuneration3 = Remuneration(
        movie_id = movie2.id,
        actor_id = actor2.id,
        remuneration = 700.00
    )
    remuneration4 = Remuneration(
        movie_id = movie2.id,
        actor_id = actor3.id,
        remuneration = 800.00
    )
    db.session.add_all([remuneration1, remuneration2,remuneration3, remuneration4])
    db.session.commit()

#https://docs.python.org/3/library/argparse.html#nargs
def getParser():
    desc='CLI tool to init db tables for capstone project based on different DB env input'
    usage=" python %(prog)s [Options] , use -h/--help or more help"
    #create a parser
    parser=argparse.ArgumentParser(description=desc, usage=usage)
    parser.add_argument('--env', dest="env",choices=['heroku','local_prod','local_test'],help='set DB env',required=True)
    #parse the args
    args = parser.parse_args()
    return args

def main():
    args=getParser()
    env=args.env
    if env == 'local_prod':
        database_path= db_path
    elif env == 'local_test':
        database_path= test_db_path
    else:
        database_path = os.getenv('DATABASE_URL', '')
        # https://stackoverflow.com/questions/62688256/sqlalchemy-exc-nosuchmoduleerror-cant-load-plugin-sqlalchemy-dialectspostgre
        if database_path.startswith("postgres://"):
            database_path = database_path.replace("postgres://", "postgresql://", 1)
    print(f"db path is : {database_path}")
    if database_path:
        init_db(database_path)
    else:
        print("database_path cannot be empty, set it in config.py for local db or DATABASE_URL for heroku deployment!! ")
if __name__=='__main__':
    main()