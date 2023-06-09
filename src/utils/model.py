from utils.logger import Logger as Logger
logger = Logger().set_logger(loggername=__name__ + '.Model').get_logger()

import enum
import json

class Model(object):
    pass

class CannteenModel(Model):

    class COURSES_TYPE(enum.Enum):
        UNDEFINED = "---undefined---"
        ENTREE = "entree" # Hauptgericht
        GARNISH = "garnish" # Beilage
        DESSERT = "dessert" # Nachspeise
        SALAT = "salat" # Snack & Salat
        NOODLE = "noodle" # Nudel
        EVENING_MENU = "evening_menu" # Abendkarte (ab 16:00 Uhr)

    class KEY_ICONS(enum.Enum):
        UNDEFINED = "---undefined---"
        PORK = "pork" # Schwein
        POULTRY = "poultry" # Geflügel
        VEGETARIAN = "vegetarian" # vegetarisch
        HOUSEMADE = "housemade" # hausgemacht
        BEEF = "beef" # Rind
        FISH = "fish" # Fisch
        ANIMAL_PRODUCTS = "animal_products" # Tier. Lab/Gelatine/Honig => tierische Erzeugnisse
        LOCAL = "local" # Regional
        SHEEP = "sheep" # Schaf
        SEAFOOD = "seafood" # Meeresfrüchte
        VEGAN = "vegan" # vegan
        HERBAL_COOKING = "herbal_cooking" # Kräuterküche
        ORGANIC = "organic" # BIO
        AOK = "aok" # Gesund durch die Woche
        VENISON = "venison" # Wild
        SUSTAINABLE_FISHING = "sustainable_fishing" # Nachhaltiger Fang
        HOME_BRAND = "home_brand" # Mensa-Vital, eine Marke der Studentenwerke
    
    ##################################################################################################################################

    def __init__(self, scrapling_timestamp=None, intended_date=None, courses_type=None, label=None, ingredients=None, icons=None, price_students=None, price_staff=None, price_guests=None, price_special_fare=None, **kwargs):
        self.id = None
        self.scrapling_timestamp = scrapling_timestamp
        self.intended_date = intended_date
        self.courses_type = courses_type
        self.label = label
        self.ingredients = ingredients
        self.icons = icons
        self.price_students = price_students
        self.price_staff = price_staff
        self.price_guests = price_guests
        self.price_special_fare = price_special_fare
        logger.debug("Model Object created")

    def __del__(self):
        pass
    
    def _getAllClassAttributes(self):
        #return [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
        logger.debug("get all class attributes")
        return self.__dict__.keys()

    ##################################################################################################################################
    #                                                                                                                                #
    #                                                       built-in types                                                           #
    #                                                                                                                                #
    ##################################################################################################################################

    # https://docs.python.org/3/reference/datamodel.html#data-model
    # https://docs.python.org/3/library/stdtypes.html#classes-and-class-instances

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.__get_cannteen_object_linear())

    ##################################################################################################################################
    #                                                                                                                                #
    #                                                      specific methods                                                          #
    #                                                                                                                                #
    ##################################################################################################################################

    def _get_model_as_dict(self):
        logger.debug("return model as dict")
        return self.__get_cannteen_object_linear()
    
    def __get_cannteen_object_linear(self):
        logger.debug("return model as linear object")
        return {
            "id" : self.id,
            "scrapling_timestamp" : self.scrapling_timestamp,
            "intended_date" : self.intended_date,
            "courses_type" : self.courses_type,
            "label" : self.label,
            "ingredients" : self.ingredients,
            "icons" : self.icons,
            "price_students" : self.price_students,
            "price_staff" : self.price_staff,
            "price_guests" : self.price_guests,
            "price_special_fare" : self.price_special_fare
        }
    
    def __get_cannteen_object_hierarchical(self):
        logger.debug("return model as hierarchical object")
        return {
            "id" : self.id,
            "scrapling_timestamp" : self.scrapling_timestamp,
            "meal" : {
                "intended_date" : self.intended_date,
                "courses_type" : self.courses_type,
                "label" : self.label,
                "ingredients" : self.ingredients,
                "icons" : self.icons,
                "price" : {
                    "price_students" : self.price_students,
                    "price_staff" : self.price_staff,
                    "price_guests" : self.price_guests,
                    "price_special_fare" : self.price_special_fare
                }
            }
        }

    def __check_hierarchical(self, hierarchical=False):
        if hierarchical is True:
            json_object = self.__get_cannteen_object_hierarchical()
        else:
            json_object = self.__get_cannteen_object_linear()
        logger.debug("return model as json object")
        return json_object
    
    ##################################################################################################################################

    def print(self, hierarchical=False):
        json_object = self.__check_hierarchical(hierarchical=hierarchical)
        line = json.dumps(obj=json_object, separators=(',', ':'), indent=4)
        logger.debug("print model")
        print(line)
        return self

    def convert_to_json(self, hierarchical=False):
        json_object = self.__check_hierarchical(hierarchical=hierarchical)
        logger.debug("convert model to json object")
        return json.dumps(json_object, separators=(',', ':'))
    
    def convert_to_dict(self, json_object):
        logger.debug("convert model to dict object")
        return json.loads(json_object)
    
    def import_model(self, datarow):
        for key, value in datarow.items():
            if isinstance(value, int):
                exec_command = 'self.%s = %d'
            elif isinstance(value, float):
                exec_command = 'self.%s = %f'
            else:
                exec_command = 'self.%s = "%s"'
            
            exec(exec_command % (key, value))
        logger.debug("Model imported")
        return self
    
    def export_model(self):
        columns = ""
        values = ""

        for key, value in self.__get_cannteen_object_linear().items():
            if key == "id":
                continue
            columns = columns + "'" + str(key) + "'" + ", "
            values = values + "'" + str(value) + "'" + ", "
            
        sql_statement = ''' INSERT INTO results (''' + columns[:-2] + ''') VALUES (''' + values[:-2] + ''') '''
        logger.debug("Model exported ['%s']", sql_statement)
        return sql_statement