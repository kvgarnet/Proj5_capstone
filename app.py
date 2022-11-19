import os
from flask import Flask, request, abort, jsonify
# from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movies, Actors,Remuneration,db
from flask_cors import CORS
import sys
from datetime import datetime
from auth.auth import AuthError, requires_auth


# format code
def format_queries(queries):
    return [query.format() for query in queries]

def validate_date(date_str):
    try:
        release_date = datetime.strptime(date_str, '%m-%d-%Y').date()
        return release_date
    except ValueError:
        print("Incorrect date string format. It should be MM-DD-YYYY")
        abort(400)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    return app

app = create_app()

'''
based on project 3
run following script before starting app to initialize  datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! ONLY NECESSARY ON FIRST RUN
'''

# init_db.py

@app.route('/')
def greeting():
    excited = os.getenv('EXCITED', None)
    greeting = "Hello"
    if excited == 'true':
        greeting = greeting + "!!!!! You are doing great in this Udacity project."
    return greeting

@app.route('/movies')
def movies():
    try:
        movies = Movies.query.order_by('id').all()
    except:
        abort(422)
    if not movies:
        abort(404)
    movies_format = format_queries(movies)
    return jsonify({
        "success": True,
        "movies": movies_format
    })

@app.route('/actors')
def actors():
    try:
        actors = Actors.query.order_by('id').all()
    except:
        abort(422)
    if not actors:
        abort(404)
    actors_format = format_queries(actors)
    return jsonify({
        "success": True,
        "actors": actors_format
    })

@app.route('/movies/new', methods=['POST'])
def create_movie():
    body = request.get_json()
    if not body:
        abort(400)
    else:
        title = body.get('title', None)
        date_str = body.get('release_date', None)
        # print(f"{date_str}")
    # both fields required
    if not (title and date_str):
        abort(422)
    # check date input format compatibility
    release_date=validate_date(date_str)
    try:
        movie = Movies(
        title=title,
        release_date=release_date
        )
        movie.insert()
        return jsonify({
            "success": True,
            "new_movie": [movie.format()]
        })
    except:
        movie.rollback()
        print(sys.exc_info())
        return abort(422)
    finally:
        movie.close()

@app.route('/actors/new', methods=['POST'])
def create_actor():
    body = request.get_json()
    if not body:
        abort(422)
    else:
        name = body.get('name', None)
        gender = body.get('gender', None)
        age = body.get('age', None)
    # all fields required
    if not (name and gender and age):
        abort(400)
    try:
        actor = Actors(
            name=name,
            gender=gender,
            age=age
        )
        actor.insert()
        return jsonify({
            "success": True,
            "actor": [actor.format()]
        })
    except:
        actor.rollback()
        print(sys.exc_info())
        return abort(422)
    finally:
        actor.close()

@app.route('/movies/<int:id>', methods=['PATCH'])
# @requires_auth(permission='patch:drinks')
def update_movies(id):
    movie = Movies.query.filter_by(id=id).one_or_none()
    # query via 'filter'
    # movie = Movies.query.filter(Movies.id == id).one_or_none()
    if not movie:
        abort(404)
    body = request.get_json()
    title = body.get('title', None)
    release_date = body.get('release_date', None)
    # either fields submitted is fine
    if not (title or release_date):
        abort(422)
    if title:
        movie.title = title
    print(f"input date is :{release_date}")
    if release_date:
        # check date input format compatibility
        # release_date=validate_date(release_date)
        validate_date(release_date)
        movie.release_date=release_date
        print(f"release date:{movie.release_date}")
    try:
        movie.update()
        return jsonify({
            "success": True,
            "movie": [movie.format()]
        })
    except:
        movie.rollback()
        print(sys.exc_info())
        return abort(422)
    finally:
        movie.close()

@app.route('/actors/<int:id>', methods=['PATCH'])
# @requires_auth(permission='patch:drinks')
def update_actors(id):
    actor = Actors.query.filter_by(id=id).one_or_none()
    if not actor:
        abort(404)
    body = request.get_json()
    name = body.get('name', None)
    gender = body.get('gender', None)
    age = body.get('age', None)
    # either fields submitted is fine
    if not (age or name or gender):
        abort(422)
    if name:
        actor.name = name
    if gender:
        actor.gender = gender
    if age:
        actor.age = age
    try:
        actor.update()
        return jsonify({
            "success": True,
            "actor": [actor.format()]
        })
    except:
        actor.rollback()
        print(sys.exc_info())
        return abort(422)
    finally:
        actor.close()

@app.route('/movies/<int:id>', methods=['DELETE'])
# @requires_auth(permission='delete:movies')
def delete_movie(id):
    movie = Movies.query.filter_by(id=id).one_or_none()
    if not movie:
        abort(404)
    try:
        movie.delete()
        return jsonify({
            "success": True,
            "deleted_movie": movie.id
        })
    except:
        movie.rollback()
        print(sys.exc_info())
        return abort(422)
    finally:
        movie.close()


@app.route('/actors/<int:id>', methods=['DELETE'])
# @requires_auth(permission='delete:actors')
def delete_actor(id):
    actor = Actors.query.filter_by(id=id).one_or_none()
    if not actor:
        abort(404)
    try:
        actor.delete()
        return jsonify({
            "success": True,
            "deleted_actor": actor.id
        })
    except:
        actor.rollback()
        print(sys.exc_info())
        return abort(422)
    finally:
        actor.close()

@app.route('/remuneration')
def get_remuneration():
    remunerations=db.session.query(Remuneration).order_by('movie_id').all()
    remuneration_format= format_queries(remunerations)
    return jsonify({
        "success": True,
        "remunerations ": remuneration_format
    })

@app.route('/remuneration',methods=['POST'])
def new_remuneration():
    body = request.get_json()
    if not body:
        abort(404)
    else:
        movie_id = body.get('movie_id', None)
        actor_id = body.get('actor_id', None)
        rem = body.get('remuneration', None)
    #check if valid movie_id and actor_id

    movie = Movies.query.filter_by(id=movie_id).one_or_none()
    actor = Actors.query.filter_by(id=actor_id).one_or_none()
    if not( movie and actor):
        abort(404)
    # all fields required
    if not (movie_id and actor_id and rem):
        abort(400)
    try:
        remuneration = Remuneration(
            movie_id=movie_id,
            actor_id=actor_id,
            remuneration=rem
        )
        remuneration.insert()
        return jsonify({
            "success": True,
            "actor": [remuneration.format()]
        })
    except:
        remuneration.rollback()
        print(sys.exc_info())
        return abort(422)
    finally:
        remuneration.close()

@app.route('/remuneration', methods=['PATCH'])
# @requires_auth(permission='patch:drinks')
def update_remuneration():
    body = request.get_json()
    movie_id = body.get('movie_id', None)
    actor_id = body.get('actor_id', None)
    rem = body.get('remuneration', None)
    # either fields submitted is fine
    if not (movie_id and actor_id):
        abort(400)
    remuneration = Remuneration.query.filter_by(movie_id=movie_id).filter_by(actor_id=actor_id).one_or_none()
    if not remuneration:
        abort(404)
    if movie_id:
        remuneration.movie_id = movie_id
    if actor_id:
        remuneration.actor_id = actor_id
    if remuneration:
        remuneration.remuneration = rem
    try:
        remuneration.update()
        return jsonify({
            "success": True,
            "remuneration": [remuneration.format()]
        })
    except:
        remuneration.rollback()
        print(sys.exc_info())
        return abort(422)
    finally:
        remuneration.close()

@app.route('/remuneration/<int:id>', methods=['DELETE'])
# @requires_auth(permission='delete:remuneration')
def delete_remuneration(id):
    remuneration = Remuneration.query.filter_by(id=id).one_or_none()
    if not remuneration:
        abort(404)
    try:
        remuneration.delete()
        return jsonify({
            "success": True,
            "deleted_remuneration": remuneration.id
        })
    except:
        remuneration.rollback()
        print(sys.exc_info())
        return abort(422)
    finally:
        remuneration.close()

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(404)
def error_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(400)
def error_bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Incorrect input format."
    }), 400




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


