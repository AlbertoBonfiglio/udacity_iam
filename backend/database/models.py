import os
import sys
from faker import Faker
from sqlalchemy import Column, String, Integer, JSON
from flask_sqlalchemy import SQLAlchemy
import json

DRINKS = [ 
    "20th century",
    "Angel face",
    "Aviation", 
    "Bee's knees",
    "Bijou",
    "Blackthorn",
    "Bloody Margaret",
    "Bramble",
    "Breakfast martini",
    "Bronx",
    "Casino",
    "Cloister"
]

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    try:
        database_filename = os.environ['APP_DB']
        project_dir = os.path.dirname(os.path.abspath(__file__))
        database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))
        
        app.config["SQLALCHEMY_DATABASE_URI"] = database_path
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.app = app
        db.init_app(app)
      #  db_drop_and_create_all();
    except Exception as err:
        # Log the error to the console
        print("Something went wrong", err)
        # rethrow it
        raise err
'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''
def db_drop_and_create_all():
    try: 
        ROWS = 7
        db.drop_all()
        db.create_all()

        # add one demo row which is helping in POSTMAN test
        for i in DRINKS:
            drink = Drink(
                title=i,
                recipe= {"data": [
                             {"name": "water", "color": "blue", "parts": 1}
                        ]}
            )
            drink.insert()
            
        print('database seeded')    
    except Exception as err:
        # Log the error to the console
        print("Something went wrong", err)
        # rethrow it
        raise err



'''
Drink
a persistent drink entity, extends the base SQLAlchemy Model
'''
class Drink(db.Model):
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # String Title
    title = Column(String(80), nullable=False,  unique=True)
    # the ingredients blob - this stores a lazy json blob
    # the required datatype is {[{'color': string, 'name':string, 'parts':number}]}
    recipe = Column(JSON, nullable=False, default={"data": []})

    '''
    short()
        short form representation of the Drink model
    '''
    def short(self):
        data = self.recipe['data']        
        short_recipe = [{'color': r['color'], 'parts': r['parts']}
                        for r in data]
        return {
            'id': self.id,
            'title': self.title,
            'recipe': short_recipe
        }

    '''
    long()
        long form representation of the Drink model
    '''
    def long(self):
        return {
            'id': self.id,
            'title': self.title,
            'recipe': self.recipe['data']
        }

    '''
    validateRecipe(self)
    '''
    def validateRecipe(self):
        # Simple validator. If any of the properties is missing in the 
        # array objects the validation fails 
        try:
            data = self.recipe['data']
            check = [
                {'color': r['color'], 'parts': r['parts'], 'name':r['name']}
                for r in data
            ]
            return True
        except Exception as err:
            print(sys.exc_info(), err)
            return False

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink.query.filter(Drink.id == id).one_or_none()
            drink.title = 'Black Coffee'
            drink.update()
    '''

    def update(self):
        # db.session.update(self)
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())
