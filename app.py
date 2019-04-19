# -*- coding: utf-8 -*-
"""
@author: hxvinh
"""

from datetime import datetime
import pytz

from flask import jsonify
from flask_restful import Resource
from flask_jwt import jwt_required

import settings

settings.init()


"""
CustomerCollection is Resource that one can perform POST/GET verbs on the whole database.
"""
class CustomerCollection(Resource):

    @jwt_required()
    def post(self):
        args = settings.customer_request_parser.parse_args()
        insert_query = 'INSERT INTO customers (name, dob, updated_at) VALUES (%s,%s,%s)'
        ist = pytz.timezone('Asia/Singapore')
        current_timestamp =  ist.localize(datetime.now()).strftime('%Y-%m-%d %H:%M:%S%z')
        record_to_insert = (args.name, args.dob, current_timestamp)
        message, result = settings.customers._database.execute_query(query_type='U', query_content=insert_query, 
                                                      arg_dict={'record_to_insert': record_to_insert,},
                                                      )
        
        return jsonify({'status_code': 201,
                        'msg': 'Customer added',})

    @jwt_required()
    def get(self):
        select_query = 'SELECT * FROM customers;'
        message, result = settings.customers._database.execute_query(query_type='R', query_content=select_query,
                                                            arg_dict={'fetch_mode': 'all', },
                                                            )

        result = [{'id': i[0], 
                   'name': i[1], 
                   'dob': i[2].strftime('%Y-%m-%d'), 
                   'updated_at': i[3].strftime('%Y-%m-%d %H:%M:%S %z')}
                    for i in result]
        
        return jsonify({'result': result,
                        'status_code': 200,
                        'msg': 'OK',})
    
    
    def put(self):
        return jsonify({'status_code': 405,
                        'msg': 'Method not allowed',})
            
            
    def patch(self):
        return jsonify({'status_code': 405,
                        'msg': 'Method not allowed',})        
        
            
    def delete(self):
        return jsonify({'status_code': 405,
                        'msg': 'Method not allowed',})

"""
Customer is Resource that one can perform GET/PUT/DELETE verbs on a particular 
user based on their id.
"""
class Customer(Resource):
    
    
    def post(self, id):
        return jsonify({'status_code': 405,
                        'msg': 'Method not allowed',})
     
        
    @jwt_required()
    def get(self, id):
        customer = settings.get_customer_by_id(id)
        if customer is None:
            return jsonify({'status_code': 404,
                            'msg': 'Customer not found'})

        return jsonify({'id': customer[0],
                        'name': customer[1],
                        'dob': customer[2].strftime('%Y-%m-%d'),
                        'updated_at': customer[3].strftime('%Y-%m-%d %H:%M:%S %z'),
                        'status_code': 200,
                        'msg': 'OK', })


    @jwt_required()
    def put(self, id):
        
        args = settings.customer_request_parser.parse_args()
        customer = settings.get_customer_by_id(id)
        if customer is None:
            return jsonify({'status_code': 404,
                            'msg': 'Customer not found'})
        
        update_query = 'UPDATE customers SET name = %s, dob = %s, updated_at = %s WHERE ID = %s;'
        ist = pytz.timezone('Asia/Singapore')
        current_timestamp =  ist.localize(datetime.now()).strftime('%Y-%m-%d %H:%M:%S%z')
        record_to_update = (args.name, args.dob, current_timestamp, id)
        message, result = settings.customers._database.execute_query(query_type='U', query_content=update_query,
                                                      arg_dict={'record_to_update': record_to_update, },
                                                      )

        return jsonify({'status_code': 200,
                        'msg': 'Customer updated'})
            
            
    def patch(self, id):
        return jsonify({'status_code': 405,
                        'msg': 'Method not allowed',}) 


    @jwt_required()
    def delete(self, id):
        customer = settings.get_customer_by_id(id)
        
        if customer is None:
            return jsonify({'status_code': 404,
                            'msg': 'Customer not found'})
        else:
            delete_query = 'DELETE FROM customers WHERE ID = %s'
            message, result = settings.customers._database.execute_query(query_type='D', query_content=delete_query,
                                                      arg_dict={'attributes': (id, )},
                                                      )

        return jsonify({'status_code': 200,
                        'msg': 'Customer deleted',})

"""
CustomerQuery is Resource that one can perform any retrieval query (GET) 
on the whole database.
"""
class CustomerQuery(Resource):
    
    def post(self):
        return jsonify({'status_code': 405,
                        'msg': 'Method not allowed',})
            
            
    @jwt_required()
    def get(self):
        args = settings.query_request_parser.parse_args()
        result = settings.customers._database.execute_flexible_query(query=args.query,
                                                               is_fetch=True,
                                                               fetch_mode='all',
                                                               )
        return jsonify({'result': result})
    
    
    def put(self):
        return jsonify({'status_code': 405,
                        'msg': 'Method not allowed',})
            
            
    def patch(self):
        return jsonify({'status_code': 405,
                        'msg': 'Method not allowed',})        
        
            
    def delete(self):
        return jsonify({'status_code': 405,
                        'msg': 'Method not allowed',})
    
    
"""
Authentication and Identity
USER_DATA: dictionary with key is username and value is password.
"""



class PrivateResource(Resource):
    @jwt_required()
    def get(self):
        return {"meaning_of_life": 42}


settings.api.add_resource(CustomerCollection, '/customers')
settings.api.add_resource(Customer, '/customers/<int:id>')
settings.api.add_resource(CustomerQuery, '/customers_query')
settings.api.add_resource(PrivateResource, '/private')

if __name__ == '__main__':
    settings.app.run(debug=True)


    
    