#!/usr/bin/python3
"""
starts a Flask web application
"""

from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)

app.register_blueprint(app_views)
CORS(app)


@app.teardown_appcontext
def downtear(self):
    '''Status of your API'''
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    '''return render_template'''
    return jsonify(error='Not found'), 404


if __name__ == "__main__":
    HOST = getenv("HBNB_API_HOST", "0.0.0.0")
    PORT = int(getenv("HBNB_API_PORT", 5000))
    app.run(debug=True, host=HOST, port=PORT, threaded=True)
