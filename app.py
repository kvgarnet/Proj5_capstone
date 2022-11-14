import os
from flask import Flask, request, abort, jsonify
# from flask_sqlalchemy import SQLAlchemy
from models import setup_db,db_drop_and_create_all,Movies,Actors,actor_remuneration
from flask_cors import CORS

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  '''
  based on project 3
  uncomment the following line to initialize the datbase
  !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
  !! ONLY NECESSARY ON FIRST RUN
  '''
  db_drop_and_create_all()

  @app.route('/')
  def get_greeting():
    excited = os.environ['EXCITED']
    greeting = "Hello"
    if excited == 'true':
      greeting = greeting + "!!!!! You are doing great in this Udacity project."
    return greeting

  @app.route('/coolkids')
  def be_cool():
    return "Be cool, man, be coooool! You're almost a FSND grad!"

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)