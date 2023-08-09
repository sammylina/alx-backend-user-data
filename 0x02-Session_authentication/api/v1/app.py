#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

auth_type = os.environ.get('AUTH_TYPE')

if auth_type == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif auth_type == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif auth_type == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()


@app.before_request
def request_validator():
    """vaidate incoming request
    IF
        - authentication header is provided
        - requested path require authentication
        - there is authorization header value
        - there is user
    """
    excluded_list = ['/api/v1/status/', '/api/v1/unauthorized/',
                     '/api/v1/forbidden/']
    if auth is None:
        return
    elif auth.require_auth(request.path, excluded_list) is False:
        return
    elif auth.authorization_header(request) is None:
        abort(401)
    current_user = auth.current_user(request)
    if current_user is None:
        abort(403)

    request.current_user = current_user


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def not_authorized(error) -> str:
    """ User not authorized
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def not_authorized(error) -> str:
    """ Request Forbidden
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
