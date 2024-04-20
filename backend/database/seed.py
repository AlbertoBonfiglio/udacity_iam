from faker import Faker
from faker.providers import lorem, python
from faker.providers import DynamicProvider

from backend.database.models import db, Drink

internet_colors_provider = DynamicProvider(
    provider_name="internet_color",
    elements=[
        'Alice Blue',
        'Antique White', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque', 'Black', 'Blanched Almond', 'Blue', 'Blue Violet',
        'Brown', 'Burlywood', 'Cadet Blue', 'Chartreuse', 'Chocolate', 'Coral', 'Cornflower Blue', 'Cornsilk', 'Crimson', 'Cyan',
        'Dark Blue', 'Dark Cyan', 'Dark Goldenrod', 'Dark Gray', 'Dark Green', 'Dark Khaki', 'Dark Magenta', 'Dark Olive Green',
        'Dark Orange', 'Dark Orchid', 'Dark Red', 'Dark Salmon', 'Dark Sea Green', 'Dark Slate Blue', 'Dark Slate Gray',
        'Dark Turquoise', 'Dark Violet', 'Deep Pink', 'Deep Sky Blue', 'Dim Gray', 'Dodger Blue', 'Firebrick', 'Floral White',
        'Forest Green', 'Fuchsia', 'Gainsboro', 'Ghost White', 'Gold', 'Goldenrod', 'Gray', 'Web Gray', 'Green', 'Web Green',
        'Green Yellow', 'Honeydew', 'Hot Pink', 'Indian Red', 'Indigo', 'Ivory', 'Khaki', 'Lavender', 'Lavender Blush', 'Lawn Green',
        'Lemon Chiffon', 'Light Blue', 'Light Coral', 'Light Cyan', 'Light Goldenrod', 'Light Gray', 'Light Green', 'Light Pink',
        'Light Salmon', 'Light Sea Green', 'Light Sky Blue', 'Light Slate Gray', 'Light Steel Blue', 'Light Yellow', 'Lime',
        'Lime Green', 'Linen', 'Magenta', 'Maroon', 'Web Maroon', 'Medium Aquamarine', 'Medium Blue', 'Medium Orchid', 'Medium Purple',
        'Medium Sea Green', 'Medium Slate Blue', 'Medium Spring Green', 'Medium Turquoise', 'Medium Violet Red', 'Midnight Blue',
        'Mint Cream', 'Misty Rose', 'Moccasin', 'Navajo White', 'Navy Blue', 'Old Lace', 'Olive', 'Olive Drab', 'Orange', 'Orange Red',
        'Orchid', 'Pale Goldenrod', 'Pale Green', 'Pale Turquoise', 'Pale Violet Red', 'Papaya Whip', 'Peach Puff', 'Peru', 'Pink',
        'Plum', 'Powder Blue', 'Purple', 'Web Purple', 'Rebecca Purple', 'Red', 'Rosy Brown', 'Royal Blue', 'Saddle Brown', 'Salmon',
        'Sandy Brown', 'Sea Green', 'Seashell', 'Sienna', 'Silver', 'Sky Blue', 'Slate Blue', 'Slate Gray', 'Snow', 'Spring Green',
        'Steel Blue', 'Tan', 'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White', 'White Smoke', 'Yellow',
        'Yellow Green',
    ],
)

ingredients_provider = DynamicProvider(
    provider_name="ingredient",
    elements=[
        'Sugar syrup', 'Lemon juice(freshly squeezed)', 'Lime juice(freshly squeezed)', 'Gin(dry)', 'Vodka', 'Aromatic bitters(e.g. Angostura)',
        'Cognac(brandy)', 'Dry vermouth', 'Rosso / rouge(sweet) vermouth', 'Orange bitters', 'Orange juice(freshly squeezed)',
        'Triple sec liqueur(e.g. Cointreau)', 'Pineapple juice', 'White(charcoal - filtered) 1 - 3 year old light rum',
        'Bourbon whiskey',
        'Egg white(pasteurised)',
        'Soda water(club soda)',
        'Tequila reposado',
        'Grenadine / pomegranate syrup',
        'Grapefruit juice(pink)',
        'Apple juice(apple cider) unsweetened & cloudy',
        'Maraschino liqueur',
        'Absinthe verte(green)',
        'Cranberry juice(sweetened)',
        'Italian red bitter liqueur(e.g. Campari)',
        'Scotch blended whisky',
        'Cream single / half and half',
        'Elderflower liqueur',
        'Brut sparkling wine(e.g. champagne)',
        'Cognac orange liqueur(e.g. Grand Marnier)',
        'Calvados & straight applejacks',
        'Rye whiskey(100 proof / 50 % alc. / vol.)',
        'Apricot(brandy) liqueur',
        'Mint leaves(fresh)',
        'Creole bitters(e.g. Peychaud`s)',
        'Gold rum 1 - 3 year old mellow light',
        'Coffee liqueur',
        'Bénédictine D.O.M. liqueur',
        'Amaretto liqueur',
        'Well - aged rum 6 - 10yr old molasses Caribbean blended',
        'Orange Curaçao liqueur',
        'Chartreuse Verte(green)',
        'Mezcal(joven)',
        'Crème de cacao liqueur(white)',
        'Cherry brandy liqueur',
        'Gentian liqueur(e.g. Suze, Salers etc)',
        'Honey syrup(3 honey to 1 water)',
        'Black raspberry liqueur(e.g. Chambord)',
        'Orgeat(almond) syrup',
        'Blanco tequila',
        'Agave syrup',
        'Saline solution',
        'Cachaça(unaged)',
        'Fino sherry',
        'Chartreuse Jaune(yellow)',
        'Ginger ale',
        'Falernum liqueur',
        'Crème de banane liqueur',
        'Lillet Blanc (or other aromatized wine)',
        'Peated Scotch whisky',
        'Maple syrup',
        'Orange - red aperitivo(e.g. Aperol)',
        'Crème de cassis liqueur',
        'Irish cream liqueur',
        'Irish blended whiskey',
        'Oude genever',
        'Tawny port',
        'Bianco vermouth',
        'Tonic water',
        'Citrus - flavoured vodka',
        'Lime cordial(sweetened lime juice)',
        'Raspberries(fresh)',
        'Galliano L`Autentico liqueur',
        'Prosecco sparkling wine',
        'Blue curaçao liqueur',
        'Peach schnapps liqueur',
        'Espresso coffee(hot)',
        'Drambuie liqueur',
        'French rouge aromatised wine(e.g. Dubonnet Red)',
        'Ginger liqueur',
        'Pisco',
        'Vanilla - flavoured vodka',
        'Chocolate bitters',
        'Limoncello liqueur',
        'Honey(fresh)',
        'Milk(whole milk / full 3 - 4 % fat)',
        'Sauvignon Blanc white wine',
        'Carciofo amaro(e.g. Cynar)',
        'White crème de menthe liqueur',
        'Melon liqueur',
        'Ginger beer',
        'Vanilla sugar syrup',
        'Sloe gin liqueur',
        'Bison grass vodka',
        'Coconut rum liqueur(35 - 40 % alc. / vol.)',
        'Amaro Montenegro',
        'Dark crème de cacao liqueur',
        'Overproof white rum',
        'Lemon - lime soda(e.g. Sprite, 7 - Up)',
        'Pedro Ximénez sherry',
    ]
)


'''
    db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''
def db_drop_and_create_all(fake: bool = True):
    try:
        ROWS = 100
        db.drop_all()
        db.create_all()

        if fake():     
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
                    "parts": fake.pyint(max_value=5)
                } for n in range(fake.pyint(max_value=5))
                ]
                words = fake.words(nb=3)
                drink = Drink(
                    title=f'{words[0]} {words[1]} {words[2]}',
                    recipe={"data": recipes}
                )
                drink.insert()

            print('database seeded')
    except Exception as err:
        # Log the error to the console
        print("Something went wrong", err)
        # rethrow it
        raise err
