# https://docs.python.org/3/library/sqlite3.html
import sqlite3

class SQLite():
    def __init__(self, db, **kwargs):
        self.__database = db
        self.__connection = self.connect(self.__database)
        
    def connect(self, db=None):
        """ create a database connection to the SQLite database specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        if db is None:
            db = self.__database
        
        try:
            self.__connection = sqlite3.connect(db)
        except sqlite3.Error as e:
            print(e)

        return self.__connection
    
    def close(self):
        self.__connection.close()

    def read_sql_file(self, file, mode='r', encoding='utf-8'):
        file = open(file, mode, encoding=encoding)
        try:
            file_content = str(file.read())
        finally:
            file.close()
        return file_content

    def execute(self, execution_statement, connection=None):
        if connection is None:
              connection = self.__connection
        
        db_cursor = connection.cursor()
        return db_cursor.execute(execution_statement)
    
    def write_data(self, sql_statement, values=None, connection=None):
        if connection is None:
              connection = self.__connection
        
        db_cursor = connection.cursor()
        if connection is None:
            db_cursor.execute(sql_statement)
        else:
            db_cursor.execute(sql_statement, values)
        connection.commit()
        #results = connection.fetchall()
        return db_cursor.lastrowid
    
    def truncate_database(self, connection=None):
        truncate_statement = self.read_sql_file("./src/backup/database/truncate_database.sql")
        return self.execute(truncate_statement)
    
    ##################################################################################################################################
    #                                                                                                                                #
    #                                                      specific methods                                                          #
    #                                                                                                                                #
    ##################################################################################################################################

    def init_database(self, connection=None):
        init_statement = self.read_sql_file("./src/backup/database/create_tables.sql")
        self.truncate_database()
        return self.execute(init_statement)
    
    def write_scraped_line(self, values, connection=None):
        sql_statement = ''' INSERT INTO results(scrapling_timestamp, intended_date, courses_type, label, ingredients, icons, price_students, price_staff, price_guests, price_special_fare) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
        return self.write_data(sql_statement, values)