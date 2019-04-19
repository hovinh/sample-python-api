# -*- coding: utf-8 -*-
"""
@author: hxvin
"""

import unittest
from postgresql_database import PostgreSQLDatabase

"""
Unit testing on PostgresSQLDatabase class.
"""
            
class TestPostgreSQLDatabase(unittest.TestCase):

    
    def setUp(self):
        self.database = PostgreSQLDatabase()
        create_table_query = '''CREATE TABLE mobile
              (ID INT PRIMARY KEY     NOT NULL,
              MODEL           TEXT    NOT NULL,
              PRICE         REAL); '''
        message, result = self.database.execute_query(query_type='C', query_content=create_table_query)
        
        
    def tearDown(self):
        
        remove_table_query = 'DROP TABLE IF EXISTS mobile;'
        message, result = self.database.execute_query(query_type='D', query_content=remove_table_query)
                
        
    def test_insert_1row(self):
        
        insert_query = 'INSERT INTO mobile (ID, MODEL, PRICE) VALUES (%s,%s,%s)'
        record_to_insert = (5, 'One Plus 6', 950)
        message, result = self.database.execute_query(query_type='U', query_content=insert_query, 
                                                      arg_dict={'record_to_insert': record_to_insert,},
                                                      )
        self.assertEqual(message, 'Table inserts 1 record(s) successfully.')
        self.assertEqual(result, None)
        
        select_query = 'SELECT * FROM mobile;'
        message, result = self.database.execute_query(query_type='R', query_content=select_query, 
                                                      arg_dict={'fetch_mode': 'all',},
                                                      )
        self.assertEqual(len(result), 1)
        
        
    def test_insert_multiplequeries_1row(self):
        
        insert_query = 'INSERT INTO mobile (ID, MODEL, PRICE) VALUES (%s,%s,%s)'
        record_to_insert = [(1, 'Apple Iphone XS', 1000), (2, 'Samsung Galaxy S9', 900),
                            (3, 'Google Pixel', 970), (4,'LG', 800), (5, 'One Plus 6', 950)]
        message, result = self.database.execute_query(query_type='U', query_content=insert_query, 
                                                      arg_dict={'record_to_insert': record_to_insert,
                                                                'is_many': True, },
                                                      )
        self.assertEqual(message, 'Table inserts 5 record(s) successfully.')
        self.assertEqual(result, None)
        
        select_query = 'SELECT * FROM mobile;'
        message, result = self.database.execute_query(query_type='R', query_content=select_query, 
                                                      arg_dict={'fetch_mode': 'all',},
                                                      )
        self.assertEqual(len(result), 5)
        
        
    def test_delete_1row(self):
        
        insert_query = 'INSERT INTO mobile (ID, MODEL, PRICE) VALUES (%s,%s,%s)'
        record_to_insert = (5, 'One Plus 6', 950)
        message, result = self.database.execute_query(query_type='U', query_content=insert_query, 
                                                      arg_dict={'record_to_insert': record_to_insert,},
                                                      )
        
        delete_query = 'DELETE FROM mobile WHERE ID = %s'
        mobile_id = 5
        message, result = self.database.execute_query(query_type='D', query_content=delete_query,
                                                      arg_dict={'attributes': (mobile_id,),},
                                                      )
        self.assertEqual(message, 'Table deletes 1 record(s) successfully.')
        self.assertEqual(result, None)
    
        select_query = 'SELECT * FROM mobile WHERE ID = %s'
        mobile_id = 5
        message, result = self.database.execute_query(query_type='R', query_content=select_query, 
                                                      arg_dict={'attributes': (mobile_id,),
                                                                'fetch_mode': 'one'},
                                                      )
        self.assertEqual(result, None)
        
        
    def test_delete_multiplequeries_1row(self):
        insert_query = 'INSERT INTO mobile (ID, MODEL, PRICE) VALUES (%s,%s,%s)'
        record_to_insert = [(1, 'Apple Iphone XS', 1000), (2, 'Samsung Galaxy S9', 900),
                            (3, 'Google Pixel', 970), (4,'LG', 800), (5, 'One Plus 6', 950)]
        message, result = self.database.execute_query(query_type='U', query_content=insert_query, 
                                                      arg_dict={'record_to_insert': record_to_insert,
                                                                'is_many': True, },
                                                      )
        
        delete_query = 'DELETE FROM mobile WHERE ID = %s'
        mobile_id = [(1, ), (5,)]
        message, result = self.database.execute_query(query_type='D', query_content=delete_query,
                                                      arg_dict={'attributes': mobile_id,
                                                                'is_many': True,},
                                                      )
        self.assertEqual(message, 'Table deletes 2 record(s) successfully.')
        self.assertEqual(result, None)
    
        select_query = 'SELECT * FROM mobile;'
        message, result = self.database.execute_query(query_type='R', query_content=select_query, 
                                                      arg_dict={'fetch_mode': 'all'},
                                                      )
        self.assertEqual(len(result), 3)

        
    def test_delete_allrows(self):
        
        insert_query = 'INSERT INTO mobile (ID, MODEL, PRICE) VALUES (%s,%s,%s)'
        record_to_insert = [(1, 'Apple Iphone XS', 1000), (2, 'Samsung Galaxy S9', 900),
                            (3, 'Google Pixel', 970), (4,'LG', 800), (5, 'One Plus 6', 950)]
        message, result = self.database.execute_query(query_type='U', query_content=insert_query, 
                                                      arg_dict={'record_to_insert': record_to_insert,
                                                                'is_many': True, },
                                                      )
        
        delete_query = 'DELETE FROM mobile;'
        message, result = self.database.execute_query(query_type='D', query_content=delete_query,)
        
        select_query = 'SELECT * FROM mobile;'
        message, result = self.database.execute_query(query_type='R', query_content=select_query, 
                                                      arg_dict={'fetch_mode': 'all', },
                                                      )
        self.assertEqual(len(result), 0)
    
    def test_update_1row(self):
        
        insert_query = 'INSERT INTO mobile (ID, MODEL, PRICE) VALUES (%s,%s,%s)'
        record_to_insert = (5, 'One Plus 6', 950)
        message, result = self.database.execute_query(query_type='U', query_content=insert_query, 
                                                      arg_dict={'record_to_insert': record_to_insert},
                                                      )
        
        update_query = 'UPDATE mobile SET PRICE = %s WHERE ID = %s'
        mobile_id = 5
        price = 970
        message, result = self.database.execute_query(query_type='U', query_content=update_query,
                                                      arg_dict={'record_to_update': (price, mobile_id, )},
                                                      )
        
        select_query = 'SELECT * FROM mobile WHERE ID = %s'
        mobile_id = 5
        message, result = self.database.execute_query(query_type='R', query_content=select_query, 
                                                      arg_dict={'attributes': (mobile_id, )},
                                                      )
        self.assertEqual(result, (5, 'One Plus 6', 970))
    
    def test_update_multiplequeries_1row(self):
        
        insert_query = 'INSERT INTO mobile (ID, MODEL, PRICE) VALUES (%s,%s,%s)'
        record_to_insert = [(1, 'Apple Iphone XS', 1000), (2, 'Samsung Galaxy S9', 900),
                            (3, 'Google Pixel', 970), (4,'LG', 800), (5, 'One Plus 6', 950)]
        message, result = self.database.execute_query(query_type='U', query_content=insert_query, 
                                                      arg_dict={'record_to_insert': record_to_insert,
                                                                'is_many': True, },
                                                      )
        
        update_query = 'UPDATE mobile SET PRICE = %s WHERE ID = %s'
        update_attributes = [(1100, 1), (1080, 2)]
        message, result = self.database.execute_query(query_type='U', query_content=update_query,
                                                      arg_dict={'record_to_update': update_attributes,
                                                                'is_many': True,},
                                                      )
        
        select_query = 'SELECT * FROM mobile WHERE PRICE >= %s'
        price = 1080
        message, result = self.database.execute_query(query_type='R', query_content=select_query,
                                                      arg_dict={'attributes': (price,),
                                                                'fetch_mode': 'all',},
                                                     )
        self.assertEqual(len(result), 2)
    
    
    def test_complex_select_query(self):
        
        insert_query = 'INSERT INTO mobile (ID, MODEL, PRICE) VALUES (%s,%s,%s)'
        record_to_insert = [(1, 'Apple Iphone XS', 1000), (2, 'Samsung Galaxy S9', 900),
                            (3, 'Google Pixel', 970), (4,'LG', 800), (5, 'One Plus 6', 950)]
        message, result = self.database.execute_query(query_type='U', query_content=insert_query, 
                                                      arg_dict={'record_to_insert': record_to_insert,
                                                                'is_many': True, },
                                                      )
        select_query = '''SELECT * 
                          FROM mobile
                          WHERE PRICE=(
                          SELECT MAX(PRICE) FROM mobile);'''
        result = self.database.execute_flexible_query(query=select_query,
                                                               is_fetch=True,
                                                               fetch_mode='all',
                                                     )
        self.assertEqual(result, [(1, 'Apple Iphone XS', 1000)])
        
       
if __name__ == "__main__":
    unittest.main()


