# -*- coding: utf-8 -*-
"""
@author: hxvinh
"""

import psycopg2

"""
PostgreSQLDatabase is a class to communicate with and execute query on database
on the server.
"""
class PostgreSQLDatabase(object):

    
    def __init__(self, 
                 user="postgres",
                 password="HoXu2nv!nh",
                 host="localhost",
                 port="5432",
                 database="postgres"):
        """
        @params:
            - user: string, username for the PostgreSQL database.
            - password: string, given by the user at the time of installing the PostgreSQL.
            - host: string, server name or Ip address on which PostgreSQL is running.
            - port: string, given by the user at the time of installing the PostgreSQL.
            - database: string, name of database to be connected to.
        """
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._database = database
        
        self._query_map = {'C': self._create_table,
                           'R': self._read_table,
                           'U': self._update_table,
                           'D': self._delete_table,}
    
        
    def _create_table(self, query, connection, cursor, arg_dict={}):
        """
        @params:
            - query: string, follows syntax of PostgreSQL.
            - connection: an instance created by psycopg2.connect.
            - cursor: an instance created by connection.cursor().
            - argdict: a dictionary. Not to be used in this method.
        @returns:
            - message: string.
            - result: None.
        """
        cursor.execute(query)
        connection.commit()
        message = 'Table is created successfully.'
        result = None
        return message, result
    
    
    def _read_table(self, query, connection, cursor, arg_dict={}):
        """
        @params:
            - query: string, follows syntax of PostgreSQL.
            - connection: an instance created by psycopg2.connect.
            - cursor: an instance created by connection.cursor().
            - argdict: a dictionary. List of usable keys:
                - 'attributes': tuple or list of tuples, determined accordlingly with 'is_many'.
                - 'is_many': boolean.
                - 'fetch_mode': ['one', 'all', int].
        @returns:
            - message: string.
            - result: tuple or list of tuples.
        """
        attributes = arg_dict.get('attributes', None)
        is_many = arg_dict.get('is_many', False)
        fetch_mode = arg_dict.get('fetch_mode', 'one')
        
        if (attributes is not None):
            if (is_many is False):
                cursor.execute(query, attributes)
            else:
                cursor.executemany(query, attributes)
            message = 'Table is read successfully.'
            
            if (fetch_mode == 'one'):
                result = cursor.fetchone()
            elif (fetch_mode == 'all'):
                result = cursor.fetchall()
            else:
                result = cursor.fetchmany(fetch_mode)
            
        else:
            cursor.execute(query)
            message = 'Entire table is read successfully.'
            if (fetch_mode == 'one'):
                result = cursor.fetchone()
            elif (fetch_mode == 'all'):
                result = cursor.fetchall()
            else:
                result = cursor.fetchmany(fetch_mode)
            
        return message, result
        
    
    def _update_table(self, query, connection, cursor, arg_dict):
        """
        @params:
            - query: string, follows syntax of PostgreSQL.
            - connection: an instance created by psycopg2.connect.
            - cursor: an instance created by connection.cursor().
            - argdict: a dictionary. List of usable keys:
                - 'record_to_insert': tuple, list of tuples, or None.
                - 'record_to_update': tuple, list of tuples, or None.
                - 'is_many': boolean.
        @returns:
            - message: string.
            - result: None.
        """
        record_to_insert = arg_dict.get('record_to_insert', None)
        record_to_update = arg_dict.get('record_to_update', None)
        is_many = arg_dict.get('is_many', False)
        
        if (record_to_insert is not None):
            if (is_many is False):
                cursor.execute(query, record_to_insert)
            else:
                cursor.executemany(query, record_to_insert)
            connection.commit()
            count = cursor.rowcount
            message = 'Table inserts ' + str(count) + ' record(s) successfully.'
            result = None
            
        elif (record_to_update is not None):
            if (is_many is False):
                cursor.execute(query, record_to_update)
            else: 
                cursor.executemany(query, record_to_update)
            connection.commit()
            count = cursor.rowcount
            message = 'Table updates ' + str(count) + ' record(s) successfully.'
            result = None
            
        else:
            raise ValueError('arg_dict must have either record_to_insert or record_to_update as key.')
            
        return message, result
    
        
    def _delete_table(self, query, connection, cursor, arg_dict={}):
        """
        @params:
            - query: string, follows syntax of PostgreSQL.
            - connection: an instance created by psycopg2.connect.
            - cursor: an instance created by connection.cursor().
            - argdict: a dictionary. List of usable keys:
                - 'attributes': tuple or list of tuples, determined accordlingly with 'is_many'.
                - 'is_many': boolean.
        @returns:
            - message: string.
            - result: None.
        """
        attributes = arg_dict.get('attributes', None)
        is_many = arg_dict.get('is_many', False)
        
        if (attributes is None):
            cursor.execute(query)
            connection.commit()
            message = 'Table is deleted successfully.'
            result = None
        else:
            if (is_many is False):
                cursor.execute(query, attributes)
            else:
                cursor.executemany(query, attributes)
            connection.commit()
            count = cursor.rowcount
            message = 'Table deletes ' + str(count) + ' record(s) successfully.'
            result = None
            
        return message, result
    
    
    def check_table_exist(self, table_name):
        """
        @params:
            - table_name: string.
        @returns:
            - check: boolean.
        """
        try:
            connection = psycopg2.connect(user=self._user, 
                                          password=self._password, 
                                          host=self._host, 
                                          port=self._port, 
                                          database=self._database)
            cursor = connection.cursor()
            cursor.execute(f'SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)',
                           (table_name,))
            check = cursor.fetchone()[0]
            
        except(Exception, psycopg2.Error) as error:
            print ('Error while connecting to PostgreSQL', error)
            
        finally:
            #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
            
        return check
    
    
    def execute_query(self, query_type, query_content, arg_dict={}, verbose=0):
        """
        @params:
            - query: string, follows syntax of PostgreSQL.
            - connection: an instance created by psycopg2.connect.
            - cursor: an instance created by connection.cursor().
            - argdict: a dictionary.
            - verbose: 0 or 1, whether to print out message in each query.
        @returns:
            - message: string.
            - result: tuple, list of tuples, or None.
        """
        if (query_type not in ['C', 'R', 'U', 'D']):
            raise ValueError("query_type must take 1 value in this list: ['C', 'R', 'U', 'D']")
            
        try:
            connection = psycopg2.connect(user=self._user, 
                                          password=self._password, 
                                          host=self._host, 
                                          port=self._port, 
                                          database=self._database)
            cursor = connection.cursor()
            command = self._query_map[query_type]
            message, result = command(query_content, connection, cursor, arg_dict)
            if (verbose != 0):
                print (message)
            
        except(Exception, psycopg2.Error) as error:
            print ('Error while connecting to PostgreSQL', error)
            
        finally:
            #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                if (verbose != 0):
                    print('PostgreSQL connection is closed.')
                    
        return message, result
                
    
    def execute_flexible_query(self, query, is_fetch=False, fetch_mode='one'):
        """
        @params:
            - query: string, follows syntax of PostgreSQL.
            - is_fetch: boolean, whether to expect returned value after the query.
            - fetch_mode': ['one', 'all', int].
        @returns:
            - result: tuple, list of tuples, or None.
        """
        try:
            connection = psycopg2.connect(user=self._user, 
                                          password=self._password, 
                                          host=self._host, 
                                          port=self._port, 
                                          database=self._database)
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            if (is_fetch is True):
                if (fetch_mode == 'one'):
                    result = cursor.fetchone()
                elif (fetch_mode == 'all'):
                    result = cursor.fetchall()
                else:
                    result = cursor.fetchmany(fetch_mode)
            else:
                result = None
                
        except(Exception, psycopg2.Error) as error:
            print ('Error while connecting to PostgreSQL', error)
            
        finally:
            #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                    
        return result        
            
            

    
# =============================================================================
# def remove():
#     database = PostgreSQLDatabase()
#     remove_table_query = 'DROP TABLE mobile;'
#     message, result = database.execute_query(query_type='D', query_content=remove_table_query)
# 
# =============================================================================
