import os
import sys
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_api import status
from flask_cors import CORS, cross_origin
from backend.auth import requires_auth
from backend.database.models import db, db_drop_and_create_all, setup_db, Drink
from backend.utils import load_config


def create_app(env=".env"):
    load_config(env)
    
    app = Flask(__name__)
    setup_db(app)
    db.session.expire_all()

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    # TODO [X]: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    '''
    #TODO [X] uncomment the following line to initialize the datbase
    !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    !! Running this funciton will add one
    '''
    db_drop_and_create_all()

    # ROUTES
    '''
    #TODO [ ] implement endpoint GET /drinks
            it should be a public endpoint
            it should contain only the drink.short() data representation
        returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
            or appropriate status code indicating reason for failure
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
            return internal_error(err)

    '''
    #TODO [ ] implement endpoint GET /drinks-detail
            it should require the 'get:drinks-detail' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
            or appropriate status code indicating reason for failure
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
    #TODO [ ] implement endpoint POST /drinks
            it should create a new row in the drinks table
            it should require the 'post:drinks' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink} where drinks is 
            an array containing only the newly created drink, 
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
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:drinks' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
            or appropriate status code indicating reason for failure
    '''
    @app.route('/api/v1.0/drinks/<int:id>', methods=['PATCH'])
    @cross_origin()
    @requires_auth('patch:drinks')
    def patch_drink(id: int):
        try:
            record: Drink = Drink.query.get(id)
            if (record is None):
                return not_found(f'Drink # {id} not found.')

            raise Exception('Not implemented yet')

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
    #TODO [ ] implement endpoint DELETE /drinks/<id> where: 
        [ ] <id> is the existing model id
        [ ] it should respond with a 404 error if <id> is not found
        [ ] it should delete the corresponding row for <id>
        [ ] it should require the 'delete:drinks' permission
        [ ] returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record or appropriate status code indicating reason for failure
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
            "message": "The request is unprocessable"
        }), 422

    return app