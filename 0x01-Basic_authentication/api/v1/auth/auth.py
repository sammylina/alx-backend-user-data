#!/usr/bin/env python3
"""Auth module
"""


from flask import request
from typing import List, TypeVar


class Auth:
    """Authentication class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Decide if authentication is required or not
        """
        if excluded_paths is None or path is None or len(excluded_paths) == 0:
            return True
        # let all path end with '/'
        if path[-1] != '/':
            path += '/'

        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """ Parse values from authorization header
        """
        authorization = request.headers.get('Authorization')
        if request is None or authorization is None:
            return None
        return authorization

    def current_user(self, request=None) -> TypeVar('User'):
        """ Provide current user, if any
        """
        return None
