import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import requires_auth, AuthError
import re
import sys
import json
from models import Actor, Movie, setup_db

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    db = setup_db(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
        
    @app.route('/')
    def home():
        return jsonify('Hello World')

    @app.route('/actors')
    def get_actors():
        actors = Actor.query.all()
        actors_formatted = [actor.format() for actor in actors]

        if len(actors) > 0:
            return jsonify({
                            'success': True,
                            'actors': actors_formatted
                            })
        else:
            return jsonify({
                            'success': True,
                            'actors': 'Actors do not available'
                            })

    @app.route('/movies')
    def get_movies():
        movies = Movie.query.all()
        movies_formatted = [movie.format() for movie in movies]

        if len(movies) > 0:
            return jsonify({
                            'success': True,
                            'movies': movies_formatted
                            })
        else:
            return jsonify({
                            'success': True,
                            'movies': 'movies do not available'
                            })

    @app.route('/actors', methods = ['POST'])
    @requires_auth('post:actors')
    def create_actor(jwt):
        error = False
        data = request.data
        data_dictionary = json.loads(data)

        try:
            name = data_dictionary['name']
            age = data_dictionary['age']
            gender = data_dictionary['gender']
            movie_id = int(data_dictionary['movie_id'])
            actor = Actor(name = name, age = age, gender = gender, movie_id = movie_id)
            actor.insert()
        except:
            error = True
            Actor.rollback()
            print(sys.exc_info())

        if error:
            abort(422)
        else:
            return jsonify({
                            'success': True,
                            'actor': actor.format()
                            })


    @app.route('/movies', methods = ['POST'])
    @requires_auth('post:movies')
    def create_movie(jwt):
        error = False
        data = request.data
        data_dictionary = json.loads(data)
        release_date = data_dictionary['release_date']
        regex_release_date = '^(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-]\d{4}$'
        match = re.search(regex_release_date, release_date)
        if not match:
            return jsonify({
                            'succes': False,
                            'error': 422,
                            'message': 'Please insert a valid date in this format dd/mm/yyy'
                            }),422
        try:
            title = data_dictionary['title']
            movie = Movie(title = title, release_date = release_date)
            movie.insert()
        except:
            error = True
            Movie.rollback()
            print(sys.exc_info())

        if error:
            abort(422)
        else:
            return jsonify({
                            'success': True,
                            'movie': movie.format()
                            })

    @app.route('/actors/<actor_id>', methods = ['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, actor_id):
        error = False

        try:
            actor = Actor.query.filter(Actor.id == int(actor_id)).first()
            actor.delete()
        except:        
            error = True
            print(sys.exc_info())
        
        if error:
            abort(404)
        else:
            return jsonify({
                            'succes': True,
                            'id_actor': actor.id
                            })

    @app.route('/movies/<movie_id>', methods = ['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, movie_id):
        error = False

        try:
            movie = Movie.query.filter(Movie.id == int(movie_id)).first()
            movie.delete()
        except:        
            error = True
            print(sys.exc_info())
        
        if error:
            abort(404)
        else:
            return jsonify({
                            'succes': True,
                            'id_movie': movie.id
                            })


    @app.route('/actors/<actor_id>', methods = ['PATCH'])
    @requires_auth('update:actors')
    def update_actor(jwt, actor_id):
        error = False
        data = request.data
        data_dictionary = json.loads(data)

        try:
            actor = Actor.query.filter(Actor.id == int(actor_id)).first()
            actor.name = data_dictionary['name']
            actor.gender = data_dictionary['gender']
            actor.movie_id = data_dictionary['movie_id']
            actor.update()
        except:        
            error = True
            print(sys.exc_info())
        
        if error:
            abort(404)
        else:
            return jsonify({
                            'succes': True,
                            'id_actor': actor.id
                            })


    @app.route('/movies/<movie_id>', methods = ['PATCH'])
    @requires_auth('update:movies')
    def update_movie(jwt, movie_id):
        error = False
        data = request.data
        data_dictionary = json.loads(data)

        try:
            movie = Movie.query.filter(Movie.id == int(movie_id)).first()
            movie.title = data_dictionary['title']
            movie.release_date = data_dictionary['release_date']
            movie.update()
        except:        
            error = True
            print(sys.exc_info())
        
        if error:
            abort(404)
        else:
            return jsonify({
                            'succes': True,
                            'id_movie': movie.id
                            })

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
                        'success': False,
                        'error': 404,
                        'message': 'Resource Not Found',
                        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                        'success': False,
                        'error': 422,
                        'message': 'Unprocessable',
                        }), 422

    @app.errorhandler(AuthError)
    def auth_error(error):
        handler = error.format()
        return jsonify(handler[0]), handler[1]

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=os.getenv('PORT',8080), debug=True)


