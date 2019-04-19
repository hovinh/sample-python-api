# -*- coding: utf-8 -*-
"""
@author: hxvinh
"""

from flask import Flask
from flask_restful import Api
from flask_restful.reqparse import RequestParser
from flask_jwt import JWT

from customer_data_model import create_original_database

"""
Authentication and Identity
"""
class User(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return "User(id='%s')" % self.id


def verify(username, password):
    if not (username and password):
        return False
    if USER_DATA.get(username) == password:
        return User(id=123)


def identity(payload):
    user_id = payload['identity']
    return {"user_id": user_id}


"""
Supporting functions
"""
def get_customer_by_id(customer_id):
    # retrieve the customer's information via their id
    select_query = 'SELECT * FROM customers WHERE id = %s;'
    message, result = customers._database.execute_query(query_type='R', query_content=select_query, 
                                                      arg_dict={'attributes': (customer_id, ),
                                                              'fetch_mode': 'one', },
                                                      )
    return result

def init():
        
    """
    Create application
    """
    global app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'super-secret'

    global api
    api = Api(app, prefix="/api/v1")

    global jwt
    jwt = JWT(app, verify, identity)
    
    """
    Create the customer_data_model database
    """
    global customers
    customers = create_original_database()


    """
    Create user data
    """
    global USER_DATA
    USER_DATA = {"hxvinh": "abc123"}


    """ 
    Define parser to be used in CustomerCollection and CustomerQuery resources
    """
    global customer_request_parser
    customer_request_parser = RequestParser(bundle_errors=True)
    customer_request_parser.add_argument("name", type=str, required=True, help="Name has to be valid string")
    customer_request_parser.add_argument("dob", type=str, required=True, help="Date has format yyyy-mm-dd")
    
    global query_request_parser
    query_request_parser = RequestParser(bundle_errors=True)
    query_request_parser.add_argument("query", required=True, help="Must follow PostgreSQL syntax")