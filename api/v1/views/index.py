#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask import jsonify
from api.v1.views import app_views

@app_views.route("/status") 
def api_status(): 
    """
    
    """
    resp = ("status": "OK")
    return resp