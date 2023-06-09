from utils.logger import Logger as Logger
logger = Logger().set_logger(loggername=__name__ + '.Database').get_logger()

# https://docs.python.org/3/library/sqlite3.html
import sqlite3

NotImplementedErrorMessage = "\n\n\t\t\t### the CRUD operations are not implemented ###\t\t\n\t\t### please use 'read_data()' and 'write_data()' instead ###\t\t\n\n"

class SQLite():

    def __init__(self, database=None, **kwargs):
        if database is None:
            self.__database = ":memory:"
        else:
            self.__database = database
        #self.__connection = self.connect(self.__database)
        #self.__cursor = self.__connection.cursor()
        logger.debug("Database Object created")

    def __del__(self):
        self.close()
        logger.debug("Database Object deleted")

    def import_database(self, database):
        if database is not None:
            self.__database = database
            logger.debug("Database imported ['%s']", database)
        return self

    def connect(self):
        """ create a database connection to the SQLite database specified by db_file
        :return: Connection object or None (if error)
        """        
        try:
            self.__connection = sqlite3.connect(self.__database)
        except sqlite3.Error as e:
            logger.exception(e)
            print(e)
            exit()

        try:
            self.__cursor = self.__connection.cursor()
        except sqlite3.Error as e:
            logger.exception(e)
            print(e)
            exit()
        
        logger.debug("Database connection opened")
        return self.__connection
        
    def close(self):
        #self.__cursor.close()
        self.__connection.close()
        logger.debug("Database connection closed")
        return self

    def read_sql_file(self, filename, mode='r', encoding='utf-8'):
        file = open(filename, mode, encoding=encoding)
        try:
            file_content = str(file.read())
        except OSError as e:
            logger.exception(e)
            print(e)
        finally:
            file.close()
        logger.debug("read sql file '%s'", filename)
        return file_content

    def execute(self, execution_statement):
        logger.debug("execute sql statement '%s'", execution_statement)
        return self.__cursor.execute(execution_statement)
    
    ##################################################################################################################################
    
    def read_data(self, sql_statement, columns=False):
        self.__cursor.execute(sql_statement)

        if columns is True:
            # https://peps.python.org/pep-0249/#cursor-attributes
            cols_name = [cursor_attributes[0] for cursor_attributes in self.__cursor.description]
            results = [dict(zip(cols_name, item)) for item in self.__cursor.fetchall()]
        else:
            results = self.__cursor.fetchall()
        logger.debug("read sql data with statement '%s' and results '%s'", sql_statement, results)
        return results
    
    def write_data(self, sql_statement, values=None):
        if values is None:
            self.__cursor.execute(sql_statement)
        else:
            self.__cursor.execute(sql_statement, values)
        self.__connection.commit()
        logger.debug("write sql data [id='%s'] with statement '%s'", self.__cursor.lastrowid, sql_statement)
        return self.__cursor.lastrowid
    
    ##################################################################################################################################

    # Create
    def create(self, sql_statement, values=None):
        raise NotImplementedError(NotImplementedErrorMessage)

    # Read
    def read(self, sql_statement):
        raise NotImplementedError(NotImplementedErrorMessage)
    
    # Update
    def update(self, sql_statement, values=None):
        raise NotImplementedError(NotImplementedErrorMessage)
    
    # Delete
    def delete(self, sql_statement):
        raise NotImplementedError(NotImplementedErrorMessage)
    
    ##################################################################################################################################
    #                                                                                                                                #
    #                                                   specific model methods                                                       #
    #                                                                                                                                #
    ##################################################################################################################################

    def init_database(self):
        self.__created_database()
        self.truncate_database()
        self.__created_tables()
        self.truncate_tables()
        logger.debug("init database")
        return self
    
    def __created_database(self):
        #TODO: create DB if not exist
        logger.debug("create database")
        return self

    def truncate_database(self):
        truncate_statement = self.read_sql_file(filename="./src/backup/database/truncate_database.sql")
        self.write_data(sql_statement=truncate_statement)
        logger.debug("truncate database")
        return self

    def __created_tables(self):
        init_statement = self.read_sql_file(filename="./src/backup/database/create_tables.sql")
        self.write_data(sql_statement=init_statement)
        logger.debug("create default tables")
        return self

    def truncate_tables(self):
        truncate_statement = self.read_sql_file(filename="./src/backup/database/truncate_tables.sql")
        self.write_data(sql_statement=truncate_statement)
        logger.debug("truncate default tables")
        return self

    ##################################################################################################################################

    def read_dataset_by_id(self, id, columns=False):
        sql_statement = ''' SELECT * FROM results WHERE id=''' + str(id) + ''' '''
        result = self.read_data(sql_statement=sql_statement, columns=columns)[0]
        logger.debug("read dataset by id='%s' and get result '%s'", id, result)
        return result
    
    def write_scraped_line(self, values):
        sql_statement = ''' INSERT INTO results (scrapling_timestamp, intended_date, courses_type, label, ingredients, icons, price_students, price_staff, price_guests, price_special_fare) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
        result = self.write_data(sql_statement=sql_statement, values=values)
        logger.debug("write dataset with vales ('%s') and get result id='%s'", values, result)
        return result