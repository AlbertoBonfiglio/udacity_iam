import datetime
import json
import os
import unittest
from unittest.mock import Mock, patch
import sqlalchemy
from flask_api import status
from backend.auth.auth import get_token_rsa_key
from backend.api.api import create_app
from backend.database.models import db_drop_and_create_all, setup_db
from backend.utils import load_config
import jwt


load_config('.env.test')

class BackendAPITestCase(unittest.TestCase):

    headers = {}

    def get_fake_token(expired = False, include_claims = True):
        encoded_jwt = jwt.encode(
                    {'some': 'payload',
                     "iss": "urn:foo",
                     "aud": "urn:bar",
                     "exp": datetime.now(tz=datetime.timezone.utc)
                     }, 
                    'secret', 
                    algorithm='HS256',
                    headers={
                        'kid': '230498151c214b788dd97f22b85410a5'
                        }
                    )
        return encoded_jwt
    
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


    # actually instead of testing the endpoits i could test the auth calls for the correct return error
    # then test the endpoints mocking errors 
    
    # or test the endpoints but mock the triggering of errors inside to see if the end results are consistent






 # TODO [X] GET /api/v1.0/drinks should get a list of drinks
    @patch('backend.auth.auth.get_token_rsa_key')
    def test_get_drinks_should_return_200(self, mock_get_keys):
        """Test should get the list of categories  """
        url = '/api/v1.0/drinks'
        
        mock_get_keys.return_value = Mock()
        mock_get_keys.return_value = {
            "keys": [
                {
                    "kty": "RSA",
                    "use": "sig",
                    "n": "zsK-yX96zK69Zdu4c2SJBwo9CrA4P2LXKVGsIoJGBRu72PYTxNIJBHyZV3sDaJFFiDoCzSqQYsUgZ9y1uk2q0zDLEWHM6chuklkyPWDim02GIpcy8ScP5BpMdizQzuPUCGyjqmltjzBnmMfOWvhDUQ3dCbVNvjYtaQBkAS3sKLpyvCVgaibAC2Se1e9_rDs-ZLo7XvGRo1N83UEhg9irYA7pM0IOaTsUKQ6V7B2-5If5t3NHFFqTpQO_kPfYFIESawly28onE5a0uumoocPIs3cqKcq6ADDDLaivSVrKnboqGdrolsRYex1nNnPVf-qaD8R_4It_HVd23xL160sZDw",
                    "e": "AQAB",
                    "kid": "HhZNVcD1ZuMTnvk7JViwD",
                    "x5t": "swTWb1LsvU6uLBBfR1aHsMxMfG0",
                    "x5c": [
                        "MIIDFzCCAf+gAwIBAgIJZxPv2XLrEt0iMA0GCSqGSIb3DQEBCwUAMCkxJzAlBgNVBAMTHmRhcnRoYmVydC11ZGFjaXR5LmF1LmF1dGgwLmNvbTAeFw0yNDAyMjkyMjQzMTBaFw0zNzExMDcyMjQzMTBaMCkxJzAlBgNVBAMTHmRhcnRoYmVydC11ZGFjaXR5LmF1LmF1dGgwLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAM7Cvsl/esyuvWXbuHNkiQcKPQqwOD9i1ylRrCKCRgUbu9j2E8TSCQR8mVd7A2iRRYg6As0qkGLFIGfctbpNqtMwyxFhzOnIbpJZMj1g4ptNhiKXMvEnD+QaTHYs0M7j1Ahso6ppbY8wZ5jHzlr4Q1EN3Qm1Tb42LWkAZAEt7Ci6crwlYGomwAtkntXvf6w7PmS6O17xkaNTfN1BIYPYq2AO6TNCDmk7FCkOlewdvuSH+bdzRxRak6UDv5D32BSBEmsJctvKJxOWtLrpqKHDyLN3KinKugAwwy2or0layp26Khna6JbEWHsdZzZz1X/qmg/Ef+CLfx1Xdt8S9etLGQ8CAwEAAaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQUUtiwqJsqghV+v3xdAQJF6QMCfhMwDgYDVR0PAQH/BAQDAgKEMA0GCSqGSIb3DQEBCwUAA4IBAQARbmnZT/+Tn7uG7HmX2hVn6gRodcotUZ4BHL8clokMFrQ2HUDk7O1J7hQp3AZ351N3VIlYFlw1CYuoya/Zat2F54krFbvZslyRPntYYwNtmpw+iOP4/km4LXySWWxApWtxAeufBtOhSjQSVh7h3XcIQqz7bfFPrX64JFrT8Jke+ny4/D8ZscbGDGFNz3fq2smaiQEHc5mx0KuoBG9XirLOhQWvtMy3qK+Dh038Tgw+058NKRFliQ0AMQRv65sx8zln3ihBa53tJ4w7wl+U26jrX3FDbPMKO3dxNDwgEVSYQqkVFSRKthj3LIehOZURwnii29eB/1KlcyoWyjMITK09"
                    ],
                    "alg": "RS256"
                }
            ]}
        
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



 # TODO [X] GET /api/v1.0/drinks with invalid token should return 401
    def test_get_drinks_should_return_401(self):
        
        print(self.get_fake_token())
        url = '/api/v1.0/drinks'
        res = self.client().get(
            url,
            headers = { 'Authorization': f'Bearer {self.get_fake_token()}' }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
