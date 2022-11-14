import os
from flask import Flask, request, abort, jsonify
# from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movies, Actors, actor_remuneration
from flask_cors import CORS
import sys
from datetime import datetime


# format code
def format_queries(queries):
    query_format = [query.format() for query in queries]
    return query_format

def validate_date(date_str):
    try:
        release_date = datetime.strptime(date_str, '%m-%d-%Y').date()
        # return release_date
    except ValueError:
        print("Incorrect date string format. It should be MM-DD-YYYY")
        abort(400)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    '''
    based on project 3
    run following script before starting app to initialize  datbase
    !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    !! ONLY NECESSARY ON FIRST RUN
    '''

    # init_db.py

    @app.route('/')
    def get_greeting():
        excited = os.environ.get('EXCITED', None)
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
        validate_date(date_str)
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

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)


