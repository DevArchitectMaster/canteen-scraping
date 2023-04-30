# https://docs.python.org/3/library/sqlite3.html
import sqlite3

class SQLite():
    def __init__(self, database, **kwargs):
        self.__database = database
        self.__connection = self.connect(self.__database)
        self.__cursor = self.__connection.cursor()

    def __del__(self):
        self.close()

    def connect(self, database=None):
        """ create a database connection to the SQLite database specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        if database is None:
            database = self.__database
        else:
            self.__database = database
        
        try:
            self.__connection = sqlite3.connect(database)
        except sqlite3.Error as e:
            print(e)
            exit()

        return self.__connection

    def close(self):
        self.__connection.close()

    def read_sql_file(self, file, mode='r', encoding='utf-8'):
        file = open(file, mode, encoding=encoding)
        try:
            file_content = str(file.read())
        except OSError as e:
            print(e)
        finally:
            file.close()
        return file_content

    def execute(self, execution_statement):
        return self.__cursor.execute(execution_statement)
    
    def write_data(self, sql_statement, values=None):
        if values is None:
            self.__cursor.execute(sql_statement)
        else:
            self.__cursor.execute(sql_statement, values)
        self.__connection.commit()
        #results = self.__connection.fetchall()
        return self.__cursor.lastrowid
    
    ##################################################################################################################################
    #                                                                                                                                #
    #                                                      specific methods                                                          #
    #                                                                                                                                #
    ##################################################################################################################################

    def truncate_database(self):
        truncate_statement = self.read_sql_file("./src/backup/database/truncate_database.sql")
        self.execute(execution_statement=truncate_statement)
        self.__connection.commit()

    def init_database(self):
        init_statement = self.read_sql_file("./src/backup/database/create_tables.sql")
        self.truncate_database(self.__connection)
        self.execute(execution_statement=init_statement)
        self.__connection.commit()
    
    def readDataSetById(self, id):
        sql_statement = ''' SELECT * FROM results WHERE id=''' + str(id) + ''' '''
        return self.execute(execution_statement=sql_statement)
    
    def write_scraped_line(self, values):
        sql_statement = ''' INSERT INTO results(scrapling_timestamp, intended_date, courses_type, label, ingredients, icons, price_students, price_staff, price_guests, price_special_fare) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
        return self.write_data(sql_statement=sql_statement, values=values)