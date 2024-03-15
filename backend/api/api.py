import os
import sys
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_api import status
from flask_cors import CORS, cross_origin
from backend.auth.auth import AuthError, requires_auth
from backend.database.models import db, db_drop_and_create_all, setup_db, Drink
from backend.utils import load_config


def create_app(env=".env"):
    app = Flask(__name__)
    # loads the environment settings 
    load_config(env)
    # set up database    
    setup_db(app)
    # makes sure there are no sessions dangling
    db.session.expire_all() 

    # Sets up cors. For the time being sets the allowed origins to all 
    CORS(app, resources={r"/api/*": {"origins": os.environ["CORS"]}})

    """
    # TODO [X]: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    '''
    #TODO [X] uncomment the following line to initialize the datbase
    !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    !! NOTE THIS ENV VARIABLE NEEDS MUST BE SET TO FALSE AFTER 1st RUN
    !! Running this function will add dummy records to the database
    '''
    if os.environ["INIT_DB"] == "True":
        db_drop_and_create_all()

    # ROUTES
    '''
    #TODO [X] implement endpoint GET /drinks
        [X] it should be a public endpoint
        [X] it should contain only the drink.short() data representation
        [X] returns status code 200 and json {"success": True, "drinks": drinks} 
            where drinks is the list of drinks or appropriate status code indicating reason for failure
    '''
    @app.route('/api/v1.0/drinks', methods=['GET'])
    @cross_origin()
    @requires_auth('get:drinks')
    def get_drinks():
        try:
            data = Drink.query.all()
            formattedData = [datum.short() for datum in data]
            # returns the formatted data or an empty array
            return jsonify({
                'success': True,
                'drinks': formattedData
            })
 
        except Exception as err:
            print(err) 
            return internal_error(err)

    '''
    #TODO [X] implement endpoint GET /drinks-detail
        [X] it should require the 'get:drinks-detail' permission
        [X] it should contain the drink.long() data representation  
        [X] returns status code 200 and json {"success": True, "drinks": drinks} 
            where drinks is the list of drinks or appropriate status code indicating reason for failure
    '''
    @app.route('/api/v1.0/drinks-detail', methods=['GET'])
    @cross_origin()
    @requires_auth('get:drinks-details')
    def get_drinks_details():
        try:
            data = Drink.query.all()
            formattedData = [datum.long() for datum in data]
            # returns the formatted data or an empty array
            return jsonify({
                'success': True,
                'drinks': formattedData
            })

        except Exception as err:
            return internal_error(err)

    '''
    #TODO [X] implement endpoint POST /drinks
        [X] it should create a new row in the drinks table
        [X] it should require the 'post:drinks' permission
        [X] it should contain the drink.long() data representation
        [X] returns status code 200 and json {"success": True, "drinks": drink} 
            where drinks is an array containing only the newly created drink, 
            or appropriate status code indicating reason for failure
    '''
    @app.route('/api/v1.0/drinks', methods=['POST'])
    @cross_origin()
    @requires_auth('post:drinks')
    def post_drink():
        try:
            body = request.get_json()  # type: ignore
            if (body == None):
                return unprocessable('Invalid or missing data.')

            record: Drink = Drink(
                title=body.get('title', '').strip(),
                recipe=body.get('recipe', '').strip()
            )
            if (record.title != '' and record.recipe != ''):
                record.insert()
            else:
                return unprocessable('Invalid or missing data.')

            return jsonify({
                'success': True,
                'drink': [record.long()]
            })

        except Exception as err:
            print(sys.exc_info(), err)
            return internal_error(err)

    '''
    #TODO [ ] implement endpoint PATCH /drinks/<id>
         where <id> is the existing model id
        [X] it should respond with a 404 error if <id> is not found
        [ ] it should update the corresponding row for <id>
        [ ] it should require the 'patch:drinks' permission
        [ ] it should contain the drink.long() data representation
        [ ] returns status code 200 and json {"success": True, "drinks": drink} 
            where drink an array containing only the updated drink or appropriate status code indicating reason for failure
    '''
    @app.route('/api/v1.0/drinks/<int:id>', methods=['PATCH'])
    @cross_origin()
    @requires_auth('patch:drinks')
    def patch_drink(id: int):
        try:
            body = request.get_json()  # type: ignore
            
            
            
            record: Drink = Drink.query.get(id)
            if (record is None):
                return not_found(f'Drink # {id} not found.')

            record: Drink = Drink(
                title=body.get('title', '').strip(),
                recipe=body.get('recipe', '').strip()
            )
            if (record.title != '' and record.recipe != ''):
                record.insert()
            else:
                return unprocessable('Invalid or missing data.')

            return jsonify({
                'success': True,
                'drink': [record.long()]
            })

        except Exception as err:
            print(sys.exc_info(), err)
            return internal_error(err)

    '''
    #TODO [X] implement endpoint DELETE /drinks/<id> where: 
        [X] <id> is the existing model id
        [X] it should respond with a 404 error if <id> is not found
        [X] it should delete the corresponding row for <id>
        [X] it should require the 'delete:drinks' permission
        [X] returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record or appropriate status code indicating reason for failure
    '''
    @app.route('/api/v1.0/drinks/<int:id>', methods=['DELETE'])
    @cross_origin()
    @requires_auth('delete:drinks')
    def delete_drink(id=int):
        try:
            record: Drink = Drink.query.get(id)
            if (record is None):
                return not_found(f'Drink # {id} not found.')

            record.delete()
            return jsonify({
                'success': True,
                'delete': id
            })

        
        except Exception as err:
            print(sys.exc_info(), err)
            return internal_error(err)


    '''
        Returns mock keys for unit testing
    '''
    @app.route('/.well-known/jwks.json', methods=['GET'])
    @cross_origin()
    @requires_auth('delete:drinks')
    def mock_keys():
        mocks = {
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
            },
            {
                "kty": "RSA",
                "use": "sig",
                "n": "w1ENBkV_ILyEshre1k6wr7heRz4tTGRRngkVIOLK7fYSxoX6evR6PUOkHooxYJvn2jfvuuQw1wDOMtWkrCchqEISIvG-_uRPSsyy5RgnbjSADeFIxjeU-nLSSS8B-6hj3FxMRvjmU4qsFfBfRJFtEYkiq2tsXYAQz232OzNbOqdS1GW_Nxm_3MoUz7gXWgwG86cWZx35zAPMsfWjAtNFQEPUZMSt8Yyz5cnnua73ekk41iYsQIDOlpoKJTCwuFK6pHd6-7YH3fe5gVPKRlbNO4gAqdR4rYkexu9OT-zW-5tdUYkNiF2CHPhJ74Z5KRtPr07YdFNhALyf-xZPeRI7eQ",
                "e": "AQAB",
                "kid": "YvOlUSHdibv1-AclPGZvw",
                "x5t": "ZbCEWg7O4lmEPe75DAjA654XfV8",
                "x5c": [
                    "MIIDFzCCAf+gAwIBAgIJD3+iRuaX7PlrMA0GCSqGSIb3DQEBCwUAMCkxJzAlBgNVBAMTHmRhcnRoYmVydC11ZGFjaXR5LmF1LmF1dGgwLmNvbTAeFw0yNDAyMjkyMjQzMTBaFw0zNzExMDcyMjQzMTBaMCkxJzAlBgNVBAMTHmRhcnRoYmVydC11ZGFjaXR5LmF1LmF1dGgwLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAMNRDQZFfyC8hLIa3tZOsK+4Xkc+LUxkUZ4JFSDiyu32EsaF+nr0ej1DpB6KMWCb59o377rkMNcAzjLVpKwnIahCEiLxvv7kT0rMsuUYJ240gA3hSMY3lPpy0kkvAfuoY9xcTEb45lOKrBXwX0SRbRGJIqtrbF2AEM9t9jszWzqnUtRlvzcZv9zKFM+4F1oMBvOnFmcd+cwDzLH1owLTRUBD1GTErfGMs+XJ57mu93pJONYmLECAzpaaCiUwsLhSuqR3evu2B933uYFTykZWzTuIAKnUeK2JHsbvTk/s1vubXVGJDYhdghz4Se+GeSkbT69O2HRTYQC8n/sWT3kSO3kCAwEAAaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQUeyP1zEdfjFPT5Lnji/jyK+hjCbkwDgYDVR0PAQH/BAQDAgKEMA0GCSqGSIb3DQEBCwUAA4IBAQAexxBevu1J8mF78kdU9b9aqfsNh2stuG+OYYb0q17NKsLRjwlZg0FOQbTxGiIc4uvD9fG/n9qLFro4sag3hDd/Kg538SlZqa5up5KLANM2OtGw8Y7CAb5ZlkG7t4sETAZR0b6vpxdz37g8xf/xwoIpjV88akMaGM79qX1BsF3uAybogAK1t7a23G7tQsKKLYIrVwzdueLBq9tIMkUMiWMm8+hVbTj32bVsyoqkRyKJq9sEDMyLEUTkdZqlF5n9KnmdzT5OJpWQNkr6unG+ERemSJVIDc4UTphNEN+LhQrgIouy/1WIPxK6ECVQ3cH14A+aE9lehd7NNJWMW+xNmoEw"
                ],
                "alg": "RS256"
            }]
        }
        return jsonify(mocks)  


    # Error Handling
    '''
    #TODO [X] implement error handlers using the @app.errorhandler(error) decorator
        each error handler should return (with approprate messages):
        jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404
    '''

    '''
    #TODO [X] implement general error handler 500
        error handler should conform to general task above
    '''
    @app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
    def internal_error(error: Exception):
        return jsonify({
            "success": False,
            "error": error.args[0],
            "message": "Internal Server Error"
        }), status.HTTP_500_INTERNAL_SERVER_ERROR

    '''
    #TODO [X] implement error handler for AuthError status.HTTP_401_UNAUTHORIZED
        error handler should conform to general task above
    '''
    @app.errorhandler(status.HTTP_400_BAD_REQUEST)
    def bad_requestd(error):
        return jsonify({
            "success": False,
            "error": error.name,
            "message": error.description
        }), status.HTTP_400_BAD_REQUEST

    @app.errorhandler(status.HTTP_401_UNAUTHORIZED)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": error.name,
            "message": error.description
        }), status.HTTP_401_UNAUTHORIZED

    '''
    #TODO [X] implement error handler for 404
        error handler should conform to general task above
    '''
    @app.errorhandler(status.HTTP_404_NOT_FOUND)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": error.name,
            "message": error.description
        }), status.HTTP_404_NOT_FOUND

    '''
    #TODO [X] implement error handler for 422 UNPROCESSABLE
        error handler should conform to general task above
    '''
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 'Unprocessable',
            "message": f"The request is unprocessable: {error.description}"
        }), 422

    return app