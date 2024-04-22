# Coffee Shop Backend <!-- omit from toc -->

## Table Of Content <!-- omit from toc -->
- [Getting Started](#getting-started)
  - [Installing Dependencies](#installing-dependencies)
    - [Python 3.7](#python-37)
    - [Virtual Environment](#virtual-environment)
    - [PIP Dependencies](#pip-dependencies)
      - [Key Dependencies](#key-dependencies)
- [Tasks](#tasks)
  - [Setup Auth0](#setup-auth0)
  - [Implement The Server](#implement-the-server)
  - [Setup the environment](#setup-the-environment)
  - [Running the server](#running-the-server)
- [Api Endpoint documentation](#api-endpoint-documentation)


## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:drinks`
   - `get:drinks-detail`
   - `post:drinks`
   - `patch:drinks`
   - `delete:drinks`
6. Create new roles for:
   - Barista
     - can `get:drinks-detail`
     - can `get:drinks`
   - Manager
     - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com).
   - Register 2 users - assign the Barista role to one and Manager role to the other.
   - Sign into each account and make note of the JWT.Auth0 needs to be configured with a default directory for the call to oauth/token to retrieve the access token to work
   - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
   - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
   - Run the collection and correct any errors.
   - TODO [] Export the collection overwriting the one we've included so that we have your proper JWTs during review!

### Implement The Server

There are `TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/__init__.py`
2. `./src/api/__init__.py`

### Setup the environment

To run the backend several environment variables need to be properly configured:
1. `FLASK_APP`: "${workspaceFolder}/backend/api/api.py",
2. `FLASK_ENV`: `development` or `production`,
3. `CORS`: by deafault is set to `*` which accepts all connection origins. Should be changed to something more restrictive for production,
4. `APP_DB`: the database name. I.E.: `database.db` for development or production, `database.test.db` for unit tests,
5. `INIT_DB`: True for resetting the database, False for using the current database. Should be set to False after the 1st run to avoid overwriting the existing DB. For unit testing it should be set to True at all times. Please note, False and True values ARE case sensitive. 
6. `AUTH0_DOMAIN`: the Auth0 custom domain for the APP,
7. `AUTH0_CLIENTID`: the Clinet ID for the Auth0 APP,
8. `AUTH0_AUDIENCE`: the audience for the Auth0 API,
9. `AUTH0_ALGORITHMS`: "['RS256']",
    
These variables can either be configured manually from within the `./backend` directory by, for example, running in the terminal:
```bash
export FLASK_APP=backend/api/api.py;
export FLASK_ENV=development;
...
```
or more conveniently by setting the `.env` and `.env.test` files. Alternatively for VSCode users the variables could be set in the `env` section of the launch.json file


Additionally the `AUTH0_TOKEN_TEST` in the `.env.test` file needs to be configured with a valid token to run the unit tests

### Running the server

From within the `./backend` directory first ensure you are working using your created virtual environment. Usually something like this:
`source /home/<username>/<project>/.venv/bin/activate` should work.

Once the python environment and the required variables are set, torun the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Api Endpoint documentation
The endpoints for the backend API are documented in the [README_API](./README_API.md) file.