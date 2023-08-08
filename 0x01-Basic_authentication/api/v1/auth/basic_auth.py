#!/usr/bin/env python3
"""basic_auth module
"""

from api.v1.auth.auth import Auth
import base64 as base


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
