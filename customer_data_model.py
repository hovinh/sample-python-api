# -*- coding: utf-8 -*-
"""
@author: hxvinh
"""

from postgresql_database import PostgreSQLDatabase
from datetime import datetime
import pytz

"""
CustomerDataModel is a wrapper of PostgreSQLDatabase, following specification of
the customer data model defined in the assignment.
"""
class CustomerDataModel(object):
    
    def __init__(self):
        self._database = PostgreSQLDatabase()
        
        
    def check_table_exist(self):
        return self._database.check_table_exist('customers')
    
        
    def create_table(self):
        
        if (self.check_table_exist() is True):
            self.delete_table()
            
        create_table_query = '''CREATE TABLE customers
              (id   SERIAL  PRIMARY KEY     NOT NULL,
              name  TEXT    NOT NULL,
              dob   DATE    NOT NULL,
              updated_at    TIMESTAMP WITH TIME ZONE); '''
        message, result = self._database.execute_query(query_type='C', query_content=create_table_query)
        
    
    def delete_table(self):
        delete_table_query = 'DROP TABLE IF EXISTS customers;'
        message, result = self._database.execute_query(query_type='D', query_content=delete_table_query)
        
        
    def execute_query(self, query_type, query_content, arg_dict={}, verbose=0):
        message, result = self._database.execute_query(query_type=query_type, 
                                                       query_content=query_content, 
                                                       arg_dict=arg_dict, 
                                                       verbose=verbose)
        return message, result
        
    
def create_original_database():
    customers_database = CustomerDataModel()
    
    customers_database.create_table()
    
    insert_query = 'INSERT INTO customers (name, dob, updated_at) VALUES (%s,%s,%s)'
    ist = pytz.timezone('Asia/Singapore')
    current_timestamp =  ist.localize(datetime.now()).strftime('%Y-%m-%d %H:%M:%S%z')
    record_to_insert = [('Abraham Lincoln', '1809-02-12', current_timestamp),
                        ('John F. Kennedy', '1917-05-29', current_timestamp),
                        ('Winston Churchill', '1874-11-30', current_timestamp),
                        ('Mohandas Karamchand Gandhi', '1869-10-02', current_timestamp),
                        ('Queen Elizabeth II', '1926-04-21', current_timestamp),
                        ('Mr. Anonymous', '1926-04-21', current_timestamp)] 
    message, result = customers_database.execute_query(query_type='U', query_content=insert_query, 
                                                      arg_dict={'record_to_insert': record_to_insert,
                                                                'is_many': True, },
                                                      )
    return customers_database
    
    
def delete_original_database():
    customers_database = CustomerDataModel()
    customers_database.delete_table()
    
if __name__ == '__main__':
    
    create_original_database()
    