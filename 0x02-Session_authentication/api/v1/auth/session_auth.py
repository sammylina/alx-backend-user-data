#!/usr/bin/env python3
""" Session auth module
"""


from api.v1.auth.auth import Auth
from flask import request


class SessionAuth(Auth):
    """ SessionAuth class, authentication user session cookie
    """
    pass
