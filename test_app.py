import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db,db_drop_and_create_all
from auth.settings import TEST_DB_NAME, DB_USER, DB_PASSWORD
from datetime import date
from config import casting_assistant,casting_director,executive_producer

# print(f"test db is: {TEST_DB_NAME}")
class CapstoneTestCase(unittest.TestCase):
    """This class represents capstone test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = TEST_DB_NAME
        self.database_path = "postgresql://{}:{}@{}/{}".format(
DB_USER,DB_PASSWORD, "localhost:5432", self.database_name)
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
#
#     """
#     TODO
#     Write at least one test for each test for successful operation and for expected errors.
#     """
    # test category
    # def test_get_movies(self):
    #     """Test get all movies """
    #     res = self.client().get('/movies',headers={'Authorization': 'Bearer ' + casting_assistant})
    #     # print(f"res: {res}")
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'],True)
    #     self.assertTrue(data['movies'])
    # def test_get_movies_not_found(self):
    #     """Test get all movies not found"""
    #     res = self.client().get('/no_movies/1000')
    #     data = json.loads(res.data)
    #     # Ensuring data passes tests as defined below
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'Resource Not Found')
    #
    # def test_get_a_movie(self):
    #     """Test get a movie """
    #     res = self.client().get('/movies/1',headers={'Authorization': 'Bearer ' + casting_assistant})
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'],True)
    #     self.assertTrue(data['movie'])
    #
    # def test_get_a_movie_not_found(self):
    #     """Test get a movies not found"""
    #     res = self.client().get('/movies/1000',headers={'Authorization': 'Bearer ' + casting_assistant})
    #     data = json.loads(res.data)
    #     # Ensuring data passes tests as defined below
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'Resource Not Found')

    # test post movies
    # def test_post_movie(self):
    #     new_movie = {
    #         "title": "You've got mails",
    #         "release_date": '12-18-1998'
    #     }
    #     res = self.client().post('/movies/new', json=new_movie,headers={'Authorization': 'Bearer ' + casting_assistant})
    #     data = json.loads(res.data)
    #     #rm newly created test movie
    #     # self.client().delete(f"/movies/{data['new_movie_id']}")
    #     # print(f"delete movie id: {data['new_movie_id']}")
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['new_movie'])
    #
    # def test_post_movie_incomplete_input(self):
    #     incomplete_movie = {
    #             "title": "You've got mails",
    #         }
    #     res = self.client().post('/movies/new', json=incomplete_movie, headers={'Authorization': 'Bearer ' + casting_assistant})
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], "Unprocessable Entity")
#
    def test_update_movie(self):
        res = self.client().patch(
            '/movies/4',
            json={'title': 'Updated movie title4'},
            headers={'Authorization': 'Bearer ' + casting_assistant})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_update_movie_404(self):
        res = self.client().patch('/movies/100000000',
                                  json={'title': '404 movie title'},
                                  headers={'Authorization': 'Bearer ' + casting_assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource Not Found')

# # test get questions
#     def test_get_questions(self):
#         """Test get all questions """
#         res = self.client().get('/questions')
#         data = json.loads(res.data)
#         # print(f"data is :{data}")
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(data['success'], True)
#         self.assertTrue(data['questions'])
#         self.assertTrue(data['categories'])
#         self.assertEqual(data['total_questions'], len(data['questions']))
#
#     def test_get_questions_not_found(self):
#         res = self.client().get('/questions?page=1000')
#         data = json.loads(res.data)
#         # Ensuring data passes tests as defined below
#         self.assertEqual(res.status_code, 404)
#         self.assertEqual(data['success'], False)
#         self.assertEqual(data['message'], 'Resource Not Found')
#
#     # test get questions per category
#     def test_get_questions_category(self):
#         res = self.client().get('/categories/6/questions')
#         data = json.loads(res.data)
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(data['success'], True)
#         self.assertTrue(data['questions'])
#         self.assertEqual(data['current_category'],6)
#         self.assertEqual(data['total_questions'], 2)
#
#     def test_get_questions_category_not_found(self):
#         res = self.client().get('/categories/1000/questions')
#         data = json.loads(res.data)
#         print(f"category not found data is :{data}")
#         # Ensuring data passes tests as defined below
#         self.assertEqual(res.status_code, 404)
#         self.assertEqual(data['success'], False)
#         self.assertEqual(data['message'], 'Resource Not Found')
#
#     # test delete question
#     def test_delete_question(self):
#         # create a dummy question to be deleted
#         dummy_question = Question(question='What is your favorite sports?',
#                                   answer='swimming',
#                                   difficulty=1,
#                                   category=1)
#         dummy_question.insert()
#         dummy_question_id=dummy_question.id
#         #delete dummy question
#         res = self.client().delete(f'/questions/{dummy_question_id}')
#         data = json.loads(res.data)
#         question = Question.query.filter(Question.id == f'{dummy_question_id}').one_or_none()
#         # print(f"question is :{question}")
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(data['success'], True)
#         self.assertEqual(data['deleted_question_id'],f'{dummy_question_id}')
#         self.assertTrue(data['total_questions'])
#         self.assertTrue(data['questions'])
#         self.assertEqual(question,None)
#
#     def test_delete_question_not_found(self):
#         res = self.client().delete('/questions/230000')
#         data = json.loads(res.data)
#         self.assertEqual(res.status_code, 404)
#         self.assertEqual(data['success'], False)
#         self.assertEqual(data['message'], 'Resource Not Found')
#

#     def test_search_questions_with_results(self):
#         res = self.client().post('/questions/search', json={'searchTerm': 'title'})
#         data = json.loads(res.data)
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(data['success'], True)
#         self.assertTrue(data['questions'])
#         self.assertEqual(data['total_questions'], 2)
#
#     def test_search_questions_without_results(self):
#         res = self.client().post('/questions/search', json={'searchTerm': 'bizarre'})
#         data = json.loads(res.data)
#         self.assertEqual(res.status_code, 404)
#         self.assertEqual(data['success'], False)
#         self.assertEqual(data['message'], 'Resource Not Found')
#
#     # test quiz
#     def test_quiz(self):
#         mysearch = {"previous_questions": [], "quiz_category": {'type': 'Art', 'id': '6'}}
#         res = self.client().post('/quizzes', json=mysearch)
#         data = json.loads(res.data)
#         print(f"quiz question id: {data}")
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(data['success'], True)
#         self.assertTrue(data['question'])
#
#     def test_quiz_incomplete_input(self):
#         mysearch = {"quiz_category": {'type': 'Art', 'id': '6'}}
#         res = self.client().post('/quizzes', json=mysearch)
#         data = json.loads(res.data)
#         self.assertEqual(res.status_code, 422)
#         self.assertEqual(data['success'], False)
#         self.assertEqual(data['message'], "Unprocessable Entity")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
