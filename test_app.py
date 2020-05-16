
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.user = os.getenv('DB_USER','postgres')
        self.password = os.getenv('DB_PASSWORD','123456789')
        self.ip_database = 'localhost'
        self.port = '5432'
        self.database_name = "capstone_test"
        self.new_actor = {
                            'name': 'Marcos',
                            'age': '20',
                            'gender': 'Male',
                            'movie_id': '1'
                            }
        self.new_movie = {
                            'title': 'Batman2',
                            'release_date': '20/10/2020'
                            }
        self.database_path = f"postgres://{self.user}:{self.password}@{self.ip_database}:{self.port}/{self.database_name}"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_create_movies(self):
        res = self.client().post('/movies', json = self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_422_create_if_can_not_create_movies_bad_date(self):
        res = self.client().post('/movies', json = {'title': 'Thor', 'release_date': '231434234'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        
    def test_create_actors(self):
        res = self.client().post('/actors', json = self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_422_create_if_can_not_create_actors(self):
        res = self.client().post('/actors', json = {'name': 'Pedro'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_update_movie(self):
        res = self.client().patch('/movies/1', json = self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id_movie'], '1')

    def test_404_patch_if_can_not_find_a_movie(self):
        res = self.client().patch('/movies/300000', json = self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_update_actor(self):
        res = self.client().patch('/actors/1', json = self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id_actor'], '1')

    def test_404_patch_if_can_not_find_a_actor(self):
        res = self.client().patch('/actors/300000', json = self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_delete_movie(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id_movie'], '1')

    def test_404_delete_if_can_not_find_a_movie(self):
        res = self.client().delete('/movies/300000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_delete_actor(self):
        res = self.client().delete('/actor/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id_actor'], '1')

    def test_404_delete_if_can_not_find_a_actor(self):
        res = self.client().delete('/actor/300000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

        
        
        
if __name__ == '__main__':
    unittest.main()