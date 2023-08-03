#!/usr/bin/env python3
"""filtered_logger module
"""

import re
from typing import List


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """obfuscate field values from message
    """
    for field in fields:
        message = re.sub(r'{}=.*?;'.format(field),
                         r'{}={}{}'.format(field, redaction, separator),
                         message)
    return message
