#!/usr/bin/env python3
"""basic_auth module
"""

from api.v1.auth.auth import Auth


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
