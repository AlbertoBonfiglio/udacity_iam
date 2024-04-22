import json
from faker import Faker
from faker.providers import lorem, python
from backend.database.fake_providers import internet_colors_provider, ingredients_provider
from backend.database.models import Drink
from backend.database.db_setup import db
'''
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''
def db_drop_and_create_all(fake: bool = True):
    try:
        ROWS = 100
        db.drop_all()
        db.create_all()

        if (fake):
            fake = Faker()
            fake.add_provider(lorem)
            fake.add_provider(python)
            fake.add_provider(internet_colors_provider)
            fake.add_provider(ingredients_provider)

            # add 100 demo rows with fake data
            for i in range(ROWS):
                recipes = [{
                    "name": fake.ingredient(),
                    "color": fake.internet_color(),
                    "parts": fake.pyint(min_value=1, max_value=5)
                } for n in range(fake.pyint(min_value=2, max_value=6))
                ]
                words = fake.words(nb=3)
                drink = Drink(
                    title=f'{words[0]} {words[1]} {words[2]}',
                    recipe= json.dumps(recipes)
                )
                drink.insert()

            print('database seeded')
    except Exception as err:
        # Log the error to the console
        print("Something went wrong", err)
        # rethrow it
        raise err
