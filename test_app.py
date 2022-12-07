import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db,Movies,Actors
from config import test_db_path
from datetime import date
from config import casting_assistant,casting_director,executive_producer

# print(f"test db is: {test_db_path}")
class CapstoneTestCase(unittest.TestCase):
    """This class represents capstone test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = test_db_path
        setup_db(self.app, self.database_path)
        # db_drop_and_create_all()
        # run python init_db.py to create table and seed init data

        #after test, below code is not required
        # binds the app to the current context
        # with self.app.app_context():
        #     self.db = SQLAlchemy()
        #     self.db.init_app(self.app)
        #     # create all tables
        #     self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass
    # test Movies
    def test_get_movies(self):
        """Test get all movies """
        res = self.client().get('/movies',
        headers={'Authorization': 'Bearer ' + casting_assistant})
        # print(f"res: {res}")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['movies'])

    def test_get_movies_not_found(self):
        """Test get all movies not found"""
        res = self.client().get('/no_movies')
        data = json.loads(res.data)
        # Ensuring data passes tests as defined below
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_get_a_movie(self):
        """Test get a movie """
        res = self.client().get('/movies/1',headers={'Authorization': 'Bearer ' + casting_assistant})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['movie'])

    def test_get_a_movie_not_found(self):
        """Test get a movies not found"""
        res = self.client().get('/movies/1000',
            headers={'Authorization': 'Bearer ' + casting_assistant})
        data = json.loads(res.data)
        # Ensuring data passes tests as defined below
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_post_movie(self):
        """Test post a movie """
        new_movie = {
            "title": "Test Post movie",
            "release_date": '12-18-1998'
        }
        res = self.client().post('/movies/new', json=new_movie,
            headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)
        #rm newly created test movie
        data_id=data['new_movie'][0]['id']
        self.client().delete(f"/movies/{data_id}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_movie'])

    def test_post_movie_without_permission(self):
        """Test post a movie without permission"""
        new_movie = {
            "title": "No permission",
            "release_date": '12-18-1998'
        }
        res = self.client().post('/movies/new', json=new_movie,
         headers={'Authorization': 'Bearer ' + casting_director})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_post_movie_incomplete_input(self):
        incomplete_movie = {
                "title": "You've got mails",
            }
        res = self.client().post('/movies/new', json=incomplete_movie, headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Bad Input format")

    def test_update_movie(self):
        res = self.client().patch(
            '/movies/30',
            json={'title': 'Director Updated movie'},
            headers={'Authorization': 'Bearer ' + casting_director})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_update_movie_without_permission(self):
        """Test update a movie without_permission"""
        res = self.client().patch(
            '/movies/4',
            json={'title': 'Updated movie title_no_permission'},
            headers={'Authorization': 'Bearer ' + casting_assistant})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_update_movie_404(self):
        res = self.client().patch('/movies/100000000',
                                  json={'title': '404 movie title'},
                                  headers={'Authorization': 'Bearer ' + casting_director})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_delete_movie(self):
        """Test delete a  movie """
        # create a dummy movie to be deleted
        dummy_movie = Movies(title='dummy movie TBD',
                            release_date='12-18-1998'
                                  )
        dummy_movie.insert()
        dummy_movie_id=dummy_movie.id
        #delete dummy movie
        res = self.client().delete(f'/movies/{dummy_movie_id}',
            headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)
        # movie = Movies.query.filter(Movies.id == dummy_movie_id).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_movie'],dummy_movie_id)

    def test_delete_movie_without_permission(self):
        """Test delete a  movie without_permission"""
        res = self.client().delete(f'/movies/3',
            headers={'Authorization': 'Bearer ' + casting_director})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_delete_movie_not_found(self):
        """Test delete a  not-found movie """
        res = self.client().delete('/movies/230000',
           headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

### test Actors ###
    def test_get_actors(self):
        """Test get all actors """
        res = self.client().get('/actors',headers={'Authorization': 'Bearer ' + casting_assistant})
        # print(f"res: {res}")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['actors'])

    def test_get_actors_not_found(self):
        """Test get all actors not found"""
        res = self.client().get('/no_actors/1000')
        data = json.loads(res.data)
        # Ensuring data passes tests as defined below
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_get_a_actor(self):
        """Test get a actor """
        res = self.client().get('/actors/1',headers={'Authorization': 'Bearer ' + casting_assistant})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['actor'])

    def test_get_a_actor_not_found(self):
        """Test get a actors not found"""
        res = self.client().get('/actors/1000',headers={'Authorization': 'Bearer ' + casting_assistant})
        data = json.loads(res.data)
        # Ensuring data passes tests as defined below
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_post_actor(self):
        """test post an actor"""
        new_actor = {
            "name": "dummy actorTBD",
            "gender": 'male',
            "age": 25
        }
        res = self.client().post('/actors/new', json=new_actor,
                                 headers={'Authorization': 'Bearer ' + casting_director})
        data = json.loads(res.data)
        # print(f"data[actor] is: {data['actor'][0]['id']}")
        data_id=data['actor'][0]['id']
        #rm newly created test actor
        self.client().delete(f'/actors/{data_id}',headers={'Authorization': 'Bearer ' + casting_director})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_post_actor_without_permission(self):
        """test post an actor without permission"""
        new_actor = {
            "name": "no_permission post actor",
            "gender": 'male',
            "age": 25
        }
        res = self.client().post('/actors/new', json=new_actor,
                                 headers={'Authorization': 'Bearer ' + casting_assistant})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_post_actor_incomplete_input(self):
        """Test post a actor of bad input """
        incomplete_actor = {
            "name": "dummy actorTBD",
            "age": 25
        }
        res = self.client().post('/actors/new', json=incomplete_actor,
            headers={'Authorization': 'Bearer ' + casting_director})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Bad Input format")

    def test_update_actor(self):
        """Test patch a actor """
        res = self.client().patch(
            '/actors/5',
            json={'name': 'Updated actor name5'},
            headers={'Authorization': 'Bearer ' + casting_director})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_update_actor_without_permission(self):
        """Test patch a actor without_permission"""
        res = self.client().patch(
            '/actors/5',
            json={'name': 'No permission Updated actor '},
            headers={'Authorization': 'Bearer ' + casting_assistant})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_update_actor_404(self):
        res = self.client().patch('/actors/100000000',
                                  json={'name': '404 actor title'},
                                  headers={'Authorization': 'Bearer ' + casting_director})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_delete_actor(self):
        """Test delete a actor """
        # create a dummy actor to be deleted
        dummy_actor = Actors(name='dummy actor TBD',
                            gender='female',
                             age=25)
        dummy_actor.insert()
        dummy_actor_id=dummy_actor.id
        #delete dummy actor
        res = self.client().delete(f'/actors/{dummy_actor_id}',
            headers={'Authorization': 'Bearer ' + casting_director})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_actor'],dummy_actor_id)

    def test_delete_actor_without_permission(self):
        """Test delete a actor without permission """
        # create a dummy actor to be deleted
        dummy_actor = Actors(name='dummy actor TBD',
                             gender='female',
                             age=25)
        dummy_actor.insert()
        dummy_actor_id = dummy_actor.id
        # delete dummy actor
        res = self.client().delete(f'/actors/{dummy_actor_id}',
              headers={'Authorization': 'Bearer ' + casting_assistant})
        data = json.loads(res.data)
        # print(f" data is {data}")
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'], 'Permission not found.')
        self.assertEqual(data['success'], False)

    def test_delete_actor_not_found(self):
        """Test delete a  not-found actor """
        res = self.client().delete('/actors/230000',
           headers={'Authorization': 'Bearer ' + casting_director})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
