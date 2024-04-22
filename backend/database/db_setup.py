import os
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

'''
    setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    try:
        database_filename = os.environ['APP_DB']
        project_dir = os.path.dirname(os.path.abspath(__file__))
        database_path = "sqlite:///{}".format(
            os.path.join(project_dir, database_filename))

        app.config["SQLALCHEMY_DATABASE_URI"] = database_path
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.app = app
        db.init_app(app)

    except Exception as err:
        # Log the error to the console
        print("Something went wrong", err)
        # rethrow it
        raise err
