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

        self.cannteen_object_linear = self.__update_cannteen_object_linear()
        
        self.cannteen_object_hierarchical = self.__update_cannteen_object_hierarchical()

    def __del__(self):
        pass

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
        return str(self.__update_cannteen_object_linear())

    ##################################################################################################################################
    #                                                                                                                                #
    #                                                      specific methods                                                          #
    #                                                                                                                                #
    ##################################################################################################################################
    
    def __update_cannteen_object_linear(self):
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
    
    def __update_cannteen_object_hierarchical(self):
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

    def __checkHierarchical(self, hierarchical=False):
        if hierarchical is True:
            json_object = self.__update_cannteen_object_hierarchical()
        else:
            json_object = self.__update_cannteen_object_linear()
        return json_object
    
    ##################################################################################################################################

    def print(self, hierarchical=False):
        json_object = self.__checkHierarchical(hierarchical=hierarchical)
        line = json.dumps(obj=json_object, indent=4)
        print(line)

    def convertToJson(self, hierarchical=False):
        json_object = self.__checkHierarchical(hierarchical=hierarchical)
        return json.dumps(json_object)
    
    def convertToDict(self, json_object):
        return json.loads(json_object)
    
    def importFromDatabase(self, datarow):
        for key, value in datarow.items():
            if isinstance(value, int):
                exec_command = 'self.%s = %d'
            elif isinstance(value, float):
                exec_command = 'self.%s = %f'
            else:
                exec_command = 'self.%s = "%s"'
            
            exec(exec_command % (key, value))
    
    def exportToDatabase(self):
        columns = ""
        values = ""

        for key, value in self.__update_cannteen_object_linear().items():
            if key is "id":
                continue
            columns = columns + str(key) + ", "
            values = values + str(value) + ", "
            
        sql_statement = ''' INSERT INTO results (''' + columns[:-2] + ''') VALUES (''' + values[:-2] + ''') '''
        return sql_statement