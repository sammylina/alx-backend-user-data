#!/usr/bin/env python3
"""filtered_logger module
"""

import re


def filter_datum(fields, redaction: str, message: str, separator: str):
    """obfuscate field values from message
    """
    for field in fields:
        message = re.sub(r'{}=.*?;'.format(field),
                         r'{}={};'.format(field, redaction),
                         message)
    return message
