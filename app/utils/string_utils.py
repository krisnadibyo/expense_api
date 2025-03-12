import re


def isemail(text: str) -> bool:
    """
    Validates if a string is a valid email address.
    
    Returns:
        bool: True if the string is a valid email, False otherwise
    """
    # Regular expression pattern for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, str(text)))