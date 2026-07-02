"""
Helper functions for ShopSmart AI
"""


def success_response(data=None, message="Success"):
    """
    Standard success API response.
    """
    return {
        "success": True,
        "message": message,
        "data": data
    }


def error_response(message="Something went wrong"):
    """
    Standard error API response.
    """
    return {
        "success": False,
        "message": message
    }