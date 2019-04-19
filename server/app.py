# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 19:19:59 2019

@author: hxvin
"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return jsonify({"message": "Hello World!"})