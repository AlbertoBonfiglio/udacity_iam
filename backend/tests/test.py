import json
import os
import unittest
import sqlalchemy
from flask_api import status
from backend.api.api import create_app
from backend.database.models import db_drop_and_create_all, setup_db
from backend.utils import load_config

load_config('.env.test')

class BackendAPITestCase(unittest.TestCase):

    headers = {}

    """This class represents the API test case"""
    @classmethod
    def setUpClass(self):
        try:
            """Define test variables and initialize app."""
           
            self.app = create_app('.env.test')
            self.client = self.app.test_client

            # sets up the test database
            setup_db(self.app)
            db_drop_and_create_all()

            self.headers = {
                'Authorization': f'Bearer {os.environ["AUTH0_TOKEN_TEST"]}'
            }

            # binds the app to the current context
            with self.app.app_context():
                self.db = sqlalchemy()
                self.db.init_app(self.app)

                # create all tables
                # self.db.create_all()
                # creates the fake data
                #remove_test_dataset(self.db)
                #create_test_dataset(self.db)
        except Exception as err:
            print(err)

    def setUp(self):
        """Executed before each test runs"""
    
    def tearDown(self):
        """Executed after each test runs"""
        pass

    @classmethod
    def tearDownClass(self):
        """Executed after the test suite runs"""
        pass

 # TODO [X] GET /api/v1.0/drinks should get a list of drinks
    def test_get_drinks_should_return_200(self):
        """Test should get the list of categories  """
        url = '/api/v1.0/drinks'
        res = self.client().get(
            url,
            headers = self.headers
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreater(len(data['drinks']), 0)
        self.assertEqual(data['success'], True)


 # TODO [X] GET /api/v1.0/drinks without token should return 422 unprocessable
    def test_get_drinks_should_return_422(self):
        """Test should get the list of categories  """
        url = '/api/v1.0/drinks'
        res = self.client().get(
            url,
            headers = { 'Authorization': f'Bearer udacity' }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
