import json
import unittest
import sqlalchemy
from flask_api import status
from backend.api import create_app
from backend.database.models import db_drop_and_create_all, setup_db


class BackendAPITestCase(unittest.TestCase):
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
        res = self.client().get(url)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        #self.assertEqual(len(data['data']), len(category_list))
        self.assertEqual(data['success'], True)
    
 # TODO [X] GET /api/v1.0/drinks without token should return 400
    def test_get_drinks_should_return_400(self):
        """Test should get the list of categories  """
        url = '/api/v1.0/drinks'
        res = self.client().get(url)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        #self.assertEqual(len(data['data']), len(category_list))
        self.assertEqual(data['success'], False)




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
