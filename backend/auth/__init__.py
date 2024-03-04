from enum import Enum
from functools import wraps
import json
import os
from flask import request, abort, Response
from flask_api import status
from jose import jwt
from urllib.request import urlopen
from backend.utils import isNoneOrEmpty

class tokenType(Enum):
    bearer = 0
    auth = 1

try: 
    AUTH0_DOMAIN = os.environ["AUTH0_DOMAIN"]
    ALGORITHMS = ['RS256']
    API_AUDIENCE = os.environ["AUTH0_AUDIENCE"]
except:
    print('error loading environment variables') 
# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

'''
#TODO [ ] implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
        10.4.1 400 Bad Request The request could not be understood by the server due to malformed syntax. The client SHOULD NOT repeat the request without modifications.
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''


def get_token_auth_header():
    # check if authorization is not in request
    if 'Authorization' not in request.headers:
        raise AuthError({
            'code': 'missing_header',
            'description': 'Authorization header cannot be empty.'
        }, status.HTTP_400_BAD_REQUEST)

    # get the token
    auth_header = request.headers['Authorization']
    header_parts = auth_header.split(' ')

    # check if token is valid
    if len(header_parts) != 2:
        raise AuthError({
            'code': 'malformed_token',
            'description': 'Authorization token is malformed.'
        }, status.HTTP_400_BAD_REQUEST)
    elif header_parts[tokenType.bearer.value].lower() != 'bearer':
        raise AuthError({
            'code': 'missing_token',
            'description': 'Bearer token is malformed or empty.'
        }, status.HTTP_400_BAD_REQUEST)

    return header_parts[tokenType.auth.value]


'''
#TODO [ ] implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''


def check_permissions(permission, payload):
    for value in payload["permissions"]:
        if (value.lower() == permission.lower()):
            return True

    raise AuthError({
        'code': 'Unauthorized',
        'description': 'Unauthorized.'
    }, status.HTTP_401_UNAUTHORIZED)


def get_token_rsa_key(header):
    rsaKey = {}
    if 'kid' not in header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, status.HTTP_400_BAD_REQUEST)
    try:
        jsonUrl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
        public_keys = json.loads(jsonUrl.read())

        for key in public_keys['keys']:
            if key['kid'] == header['kid']:
                rsaKey = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }
    except Exception as err:
        raise AuthError({
            'code': 'invalid_header',
            'description': f'Authorization malformed. {err}'
        }, status.HTTP_400_BAD_REQUEST)

    return rsaKey


'''
#TODO [ ] implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    X it should be an Auth0 token with key id (kid)
    X it should verify the token using Auth0 /.well-known/jwks.json
    X it should decode the payload from the token
      it should validate the claims
    X return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''


def verify_decode_jwt(token=''):
    if isNoneOrEmpty(token):
        raise AuthError({
            'code': 'invalid_token',
            'description': 'Token cannot be empty.'
        }, status.HTTP_400_BAD_REQUEST)
    try:
        # Get the token header data
        header = jwt.get_unverified_header(token)

        # Make sure a Key is present in the header
        rsaKey = get_token_rsa_key(header)
        if rsaKey:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsaKey,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )
            return payload

    except jwt.ExpiredSignatureError:
        raise AuthError({
            'code': 'token_expired',
            'description': 'Token expired.'
        }, 401)

    except jwt.JWTClaimsError:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Incorrect claims. Please, check the audience and issuer.'
        }, 401)

    except Exception:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to parse authentication token.'
        }, 400)


'''
#TODO [ ] implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
              token = get_token_auth_header()
              payload = verify_decode_jwt(token)
              check_permissions(permission, payload)
            except AuthError as err:
              print(err)  # for console debugging
              abort(err.status_code)

            except Exception as err:
              abort(500)

            return f(*args, **kwargs)

        return wrapper
    return requires_auth_decorator
