#!/usr/bin/env python3
"""basic_auth module
"""

from api.v1.auth.auth import Auth
import base64 as base
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """BasicAuth class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extract base64 authorization
        """
        if authorization_header is None:
            return None
        elif type(authorization_header) != str:
            return None
        elif not authorization_header.startswith('Basic '):
            return None
        else:
            return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(
                                   self,
                                   base64_authorization_header: str) -> str:
        """ Decode base64 authorization header
        """
        if base64_authorization_header is None:
            return None
        elif type(base64_authorization_header) is not str:
            return None
        try:
            decoded = base.b64decode(base64_authorization_header)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
                    self,
                    decoded_base64_authorization_header: str) -> (str, str):
        """ Extract user
        """
        if decoded_base64_authorization_header is None:
            return None, None
        elif type(decoded_base64_authorization_header) is not str:
            return None, None
        elif decoded_base64_authorization_header.count(':') != 1:
            return None, None
        username, password = decoded_base64_authorization_header.split(':')

        return username, password

    def user_object_from_credentials(
                        self,
                        user_email: str,
                        user_pwd: str) -> TypeVar('User'):
        """ Get user instance based on email and password
        """
        if user_email is None or user_pwd is None:
            return None
        elif type(user_email) is not str or type(user_pwd) is not str:
            return None

        try:
            search_user = User.search({'email': user_email})
        except Exception:
            return None

        if len(search_user) > 0 and search_user[0].is_valid_password(user_pwd):
            return search_user[0]

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Load current user using Basic authentication
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        b64_auth_header = self.extract_base64_authorization_header(auth_header)
        if b64_auth_header is None:
            return None

        decoded_auth = self.decode_base64_authorization_header(b64_auth_header)
        if decoded_auth is None:
            return None

        username, password = self.extract_user_credentials(decoded_auth)
        if username is None or password is None:
            return None

        user = self.user_object_from_credentials(username, password)
        if user is None:
            return None

        return user
