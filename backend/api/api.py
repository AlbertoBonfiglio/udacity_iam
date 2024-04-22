import os
import sys
import json
from flask import Flask, request, jsonify
from flask_api import status
from flask_cors import CORS, cross_origin
from sqlalchemy.sql import text
from sqlalchemy import func
from backend.auth.auth import requires_auth
from backend.database.db_setup import db, setup_db
from backend.database.seeder import db_drop_and_create_all
from backend.database.models import Drink
from backend.utils import load_config


# TODO [ ] Update postman with tests and token

def create_app(env=".env"):
    print('Creating Flask App')
    app = Flask(__name__)
    # loads the environment settings 
    load_config(env)
    # set up database    
    setup_db(app)
    # makes sure there are no sessions dangling
    db.session.expire_all() 
    
    '''
    #TODO [X] uncomment the following line to initialize the datbase
    !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    !! NOTE THIS ENV VARIABLE NEEDS MUST BE SET TO FALSE AFTER 1st RUN
    !! Running this function will add dummy records to the database
    '''
    if os.environ["INIT_DB"] == "True":
        print('Seeding Database')
        db_drop_and_create_all()



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
    def get_drinks():
        try:
            data = Drink.query.order_by(Drink.title.asc()).all()
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
            data = Drink.query.order_by(Drink.title.asc()).all()
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
                recipe=json.dumps(body.get('recipe', []))
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
    #TODO [X] implement endpoint PATCH /drinks/<id>
         where <id> is the existing model id
        [X] it should respond with a 404 error if <id> is not found
        [X] it should update the corresponding row for <id>
        [X] it should require the 'patch:drinks' permission
        [X] it should contain the drink.long() data representation
        [X] returns status code 200 and json {"success": True, "drinks": drink} 
            where drink an array containing only the updated drink or appropriate status code indicating reason for failure
    '''
    @app.route('/api/v1.0/drinks/<int:id>', methods=['PATCH'])
    @cross_origin()
    @requires_auth('patch:drinks')
    def patch_drink(id: int):
        try:
            canUpdate = False;
            body = request.get_json()  # type: ignore
            
            title = body.get('title', '')
            recipe = body.get('recipe', [])
            
            record: Drink = Drink.query.get(id)
            if (record is None):
                return not_found(f'Drink # {id} not found.')

            if (title.strip() != ''):    
                record.title == title
                canUpdate = True
            
            if len(recipe) > 0:
                record.recipe = json.dumps(recipe)
                canUpdate = True
            else:
                return unprocessable('A drink must have at least one ingredient.')
            
            if (record.validateRecipe() == False): 
                return unprocessable(f'Invalid data: recipe')

            if (canUpdate):
                record.update();
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

    """
    #TODO [X]: Create a POST endpoint to get drinks based on a ingrediends term.
    It should return any drink for whom the search term  is a substring of the recipe.

    
    """
    @app.route('/api/v1.0/drinks/search', methods=['POST'])
    @cross_origin()
    def find_drinks():
        try:
            body = request.get_json()  # type: ignore
            if (body is None):
                return unprocessable('No search string provided')

            search = body.get('search', None)

            if (search is None):
                return unprocessable('No search string provided')

            # cleans up the string
            search = search.strip()
            result = []
            if (search != ''):  # No point serarching for nothing
                result = Drink.query \
                    .filter(Drink.recipe.ilike(f'%{search}%'))\
                    .all()

            formattedData = [datum.long() for datum in result]

            return jsonify({
                'success': True,
                'query': search,
                'drinks': formattedData,
                'found': len(formattedData)
            })

        except Exception as err:
            print(sys.exc_info(), err)
            return internal_error(err)


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
            "error": error,
            "message": 'Resource not found'
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
            "message": f"The request is unprocessable: {error}"
        }), 422

    return app