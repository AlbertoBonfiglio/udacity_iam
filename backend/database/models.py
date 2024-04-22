import sys
from backend.database.db_setup import db 
from sqlalchemy import Column, String,VARCHAR, Integer
import json


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
    recipe = Column(VARCHAR, nullable=True)

    '''
    short()
        short form representation of the Drink model
    '''
    def short(self):
        data = json.loads(self.recipe)
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
        test = json.loads(self.recipe)
        return {
            'id': self.id,
            'title': self.title,
            'recipe': json.loads(self.recipe)
        }

    '''
    validateRecipe(self)
    '''
    def validateRecipe(self):
        # Simple validator. If any of the properties is missing in the 
        # array objects the validation fails 
        try:
            data = json.loads(self.recipe)
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
