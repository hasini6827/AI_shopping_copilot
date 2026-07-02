"""
Validation functions
"""

import re


def validate_email(email):

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    return bool(re.match(pattern, email))


def validate_password(password):

    """
    Minimum:
    8 characters
    """

    return len(password) >= 8


def validate_search_query(query):

    if not query:
        return False

    if len(query.strip()) < 2:
        return False

    return True